# My offline documentation

## Issue of determining what attack to use
Getting all possible attacks isn't hard, what is hard is determining what is the best next possible attack to use. We could...
- Use markov decision chains, computationally very intensive probably

But we may not even be forced to use decision chains as we are following a killchain to get reach certain milestones

Though, using the idea of reaching certain milestones as a method would be okay, but would require going back to start.

I guess it's just how sometimes attacks try the leads they find, learn, and restart using new info


What if I just make it run the first attack it finds it meets the prereqs for, then iterate. Would have to keep a log of attempted attacks, consider them exhausted

There could be some things wrong with that method that I may just not be considering right now.

The way this is currently setup means that it will exhaust 1 client, then move on. It won't try multiple clients.

## Needed refactoring
Client has 2 classes, ClientData and C2Clients
This should be the new setup, as data shouldn't store the c2clients