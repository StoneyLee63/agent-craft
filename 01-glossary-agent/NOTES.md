# NOTES

The first call came back `end_turn` because Claude had no tools yet. This matters because I didn't create the loop for it to continue so it just finished its answer in one go. 

Both `TOOLS` and the code that searches `GLOSSARY` plus `lookup_term` had to get wired together. `TOOLS` existed in the file but Claude couldn't see it so I added `tools=TOOLS` to the call. So Claude sends a `tool_use` block, the loop calls `lookup_term`.

`tool_use` meant Claude stopped to ask not that the tool already ran, that was a mistake on my part. 

Once the cap at 1 proved to work I set `MAX_TURNS` to 5 for a safety net. I tested it at one because that represented the tripwire and if it proved right, which it did, then I could trust that at 5 it would stop the loop instead of keep going. At 5 rounds Claude can ask for the tool and allow the answer to return. 

Claude tested the `subagent` then tested `sub-agent` and finally `agent` at once, which exposed the separate-message problem and led to batching. Claude retried on its own which is interesting. Only the `agent` came back as a term with a definition in the glossary, the others did not. I changed how the results go back. 