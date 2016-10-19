# edgenews


This project is an exercise in architecture. More specifically it aims at implementing
the thoughts shared by Robert Martin under the name Clean Architecture.

The premise of the Clean Architecture is to resist the temptation of
building your application around your infrastructure and frameworks. After all,
what is the benefit of a micro-framework if you are still tightly coupled to it?

The benefits of this are plenty but testability without mocking and optionality
of switching out technologies in the future are the main ones.

This is achieved by layering your application like an onion. The inner layers
are more high-level and abstract, speaking the language of the problem domain
while the outer layers are more concrete, being concerned with the details of
the outside world.

The core idea underlying this architecture is the Dependency Rule. It states,
that software dependencies (imports in Python lingo) are only allowed to point inwards.
