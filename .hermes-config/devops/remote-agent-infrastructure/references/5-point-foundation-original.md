# 5-Point Foundation — Original Post

Source: Viral anonymous post from agentic-coding communities, circa 2026.

Full text as encountered:

> anyone thinking about, learning, or already working with agentic systems, you should know this.
>
> the first few steps of your setup matter more than any model or framework you pick later. get them right and you never lose your flow.
>
> the foundation nobody posts about:
> 1. tailscale. a private mesh network across every machine you own. laptop, desktop, rented node, all on one secure tailnet, reachable from anywhere. nothing else works well until this does.
> 2. termux, over that tailnet. one SSH client that reaches every node, phone included. you are never away from your stack.
> 3. tmux. persistent sessions. disconnect, close the laptop, come back, every session exactly where you left it. agentic work runs long, your terminal has to survive that.
> 4. a private git repo. the one i am most glad i found. it is the memory layer across all my agents, they pull, they work, they merge back, the codebase stays alive between sessions. context that would die in a chat window lives in the repo instead.
> 5. script everything from day one. ssh aliases for every node, setup scripts, the boring boilerplate automated. if you will do a thing more than twice, it is a script.
>
> everything past these five is decorative. know these cold.
>
> and the habit that ties it together: ask the AI itself. for the config, for the error, for any of it, let the agent do the lifting, then double check what it hands you.
>
> lock the five, build the habit, and you make it. skip it, anon, and you ngmi.

## Correction Applied in This Skill

The original post said "termius" — this is a common error. **Termux** (F-Droid Android terminal) is the correct tool. Termius is a separate proprietary SSH client. The distinction matters: Termux makes the phone a compute node on the mesh; Termius only makes it a thin remote client.
