#### Commands

* add environment to config
  ```shell
  ftbx connect "https://devstaging.flex.daletdemos.com" username password
  ```

* connect to a known environment (must be in `environments.json`)
  ```shell
  # Full URL
  ftbx connect "https://devstaging.flex.daletdemos.com"
  
  # Partial URL
  ftbx connect "daletdemos.com"
  ftbx connect "devstaging.flex"
  
  # Alias
  ftbx connect "dalet-sandbox"
  ```
* show default env
  ```shell
  ftbx env
  ```
  
* create action (locally)
  ```shell
  # Creates an action called "set-asset-status"
  ftbx create_action set-asset-status
  ```

* list config items (workflowDefinitions, actions..) and their ids
  ```shell
  # List actions and their ids
  ftbx list actions

  # List actions containg "set" and their ids
  ftbx list actions --contains set
  ```
  > available items are: [
    'accounts',
    'actions',
    'eventHandlers',
    'groups',
    'messageTemplates',
    'metadataDefinitions',
    'profiles',
    'resources',
    'roles',
    'tags',
    'taskDefinitions',
    'taxonomies',
    'timedActions',
    'userDefinedObjectsTypes',
    'variants',
    'wizards',
    'workflowDefinitions',
    'workspaces'
]