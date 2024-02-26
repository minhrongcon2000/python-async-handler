# python-async-handler

This project aims to provide a way to integrate QueueHandler to Python with lower version than 3.12.

## Context

One day, I made an attempt to write a logging SDK for my company and realize that PYTHON LOGGING IS BLOCKING OPERATION. You heard it right! They're blocking operation, which means that if you're running a Python web framework such as django or flask, you may be screwed if you're using a remote log collection server. In version 3.2, Python added [QueueHandler](https://docs.python.org/3/library/logging.handlers.html#queuehandler) and [QueueListener](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.QueueListener) to help with this issue, but it cannot be configured using properties file (Java, C#, and other high-level programming languages did this long ago). It is not until version 3.12 that Python finally added configuration for these two classes, but I think it was too late. I believe there are a lot of systems running Python below 3.12 now, so that's why I wrote this integration to make dev life easier.

## Inspiration

I took inspiration from a [blog](https://rob-blackbourn.medium.com/how-to-use-python-logging-queuehandler-with-dictconfig-1e8b1284e27a) post by Rob Blackbourn. However, his code does not take into account for the fact that `ConvertingList` wraps built-in `list` and not convert string to handlers. That's why I kinda "stole" his code and made it work.

## Usage

### For copy-paste developer

All you need to do is to copy `async-handler` and config it with your project (of course, copy-paste is pro, so they need to do extra setup).

### For lazy developer

TBA
