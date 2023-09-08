#### Commands

* add environment to config
    ```shell
    python ftbx.py connect "https://devstaging.flex.daletdemos.com" username password
    ```

* connect to a known environment (must be in `environments.json`)
    ```shell
    # Full URL
    python ftbx.py connect "https://devstaging.flex.daletdemos.com"
  
    # Partial URL
    python ftbx.py connect "daletdemos.com"
    python ftbx.py connect "devstaging.flex"
  
    # Alias
    python ftbx.py connect "dalet-sandbox"
    ```
* show default env
    ```shell
    python ftbx.py env
    ```