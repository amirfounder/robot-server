# High Level Server-Extension Communication Process

```
- Server opens a new tab
- Extension launches content script in new tab and opens socket connection with Server
- Extension initiates `register-socket` method with the URL of the tab as the identifier
- Server initiates `perform-task` method with the task conditional to the URL

(loop)

    - Extension initiates `save-data` method with the appropriate tag for the server to save

    (if message contains self-destruct tag)

        - Server sends `self-destruct` command
```