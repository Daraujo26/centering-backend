def extract_centering(utterances, clusters, tokens):
    results = []
    relations = []
    token_positions = [0]

    # Calculate token positions
    for token in tokens:
        token_positions.append(token_positions[-1] + len(token) + 1)

    prev_Cf = []
    abstract_reference_mapping = {}

    def get_anchor_word_index_in_utterance(utterance: str, mention: str):
        """
        Return the index of the anchor word of 'mention' in 'utterance'.
        We pick the last word of the mention as the anchor.
        """
        utterance_words = utterance.split()
        mention_words = mention.split()
        anchor_word = mention_words[-1].strip('.,!?').lower()

        for idx, w in enumerate(utterance_words):
            if w.strip('.,!?').lower() == anchor_word:
                return idx
        return None

    for i, utterance in enumerate(utterances):
        forward_looking = []
        utterance_start = sum(len(u) + 1 for u in utterances[:i])
        utterance_end = utterance_start + len(utterance)

        # Identify forward-looking centers (Cf)
        for cluster in clusters:
            for span in cluster:
                span_start, span_end = span
                token_start_offset = token_positions[span_start]
                token_end_offset = token_positions[span_end + 1] - 1
                if utterance_start <= token_start_offset <= utterance_end:
                    mention = " ".join(tokens[span_start:span_end + 1]).strip()
                    if mention not in forward_looking:
                        forward_looking.append(mention)
                        # Map abstract references dynamically
                        if (len(prev_Cf) > 0 and len(mention.split()) == 2 
                            and mention.split()[0].lower() in {"this", "that", "these", "those"}):
                            abstract_reference_mapping[mention] = prev_Cf[0]

        # Identify backward-looking center (Cb)
        backward_looking = None
        chosen_current_mention = None
        foundCb = False  # Track if we've assigned Cb already

        # Check clusters for overlaps
        for cluster in clusters:
            mentions_in_prev_Cf = [
                " ".join(tokens[start:end + 1]).strip()
                for start, end in cluster
                if " ".join(tokens[start:end + 1]).strip() in prev_Cf
            ]
            mentions_in_current_Cf = [
                " ".join(tokens[start:end + 1]).strip()
                for start, end in cluster
                if " ".join(tokens[start:end + 1]).strip() in forward_looking
            ]

            # If there are overlapping mentions, link them
            if mentions_in_prev_Cf and mentions_in_current_Cf:
                # The first such overlap defines the Cb (if not set yet)
                if not foundCb:
                    backward_looking = mentions_in_prev_Cf[0]
                    chosen_current_mention = mentions_in_current_Cf[0]
                    foundCb = True

                # Create relations for each overlapping pair
                # We link each mention_in_current_Cf to a corresponding mention_in_prev_Cf
                # For simplicity, let's just link the first mention_in_prev_Cf to each mention_in_current_Cf.
                # If you want a 1-to-1 mapping, you'd need more complex logic.
                for cur_mention in mentions_in_current_Cf:
                    # Find the most recent previous utterance containing backward_looking or cur_mention
                    # Actually, we need to find the mention in prev Cf that corresponds. We'll pick the first in mentions_in_prev_Cf for simplicity.
                    prev_mention = mentions_in_prev_Cf[0]

                    # Find the most recent occurrence of prev_mention in previous results
                    for prev_index in range(i - 1, -1, -1):
                        prev_result = results[prev_index]
                        if prev_mention in prev_result["Cf"]:
                            source_word_index = get_anchor_word_index_in_utterance(
                                results[prev_index]["sentence"], prev_mention
                            )
                            target_word_index = get_anchor_word_index_in_utterance(
                                utterance, cur_mention
                            )
                            if source_word_index is not None and target_word_index is not None:
                                relations.append({
                                    "sourceId": f"word-{prev_index}-{source_word_index}",
                                    "targetId": f"word-{i}-{target_word_index}",
                                    "sourceAnchor": "bottom",
                                    "targetAnchor": "top",
                                })
                            break

        # Handle abstract references if no direct backward_looking found
        if not foundCb:
            for mention in forward_looking:
                if mention in abstract_reference_mapping:
                    backward_looking = abstract_reference_mapping[mention]
                    chosen_current_mention = mention
                    foundCb = True
                    # No break; abstract references only define one backward_looking mention anyway.
                    break

        # Handle possessives
        if not foundCb:
            for mention in forward_looking:
                if mention.lower() in {"his", "her", "their", "its"} and prev_Cf:
                    backward_looking = prev_Cf[0]
                    chosen_current_mention = mention
                    foundCb = True
                    break

        results.append({
            "sentence": utterance,
            "Cf": forward_looking,
            "Cb": backward_looking
        })
        prev_Cf = forward_looking

    return {
        "results": results,
        "relations": relations
    }
