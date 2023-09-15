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

* pull actions
  ```shell
  # Pull **ALL** actions
  ftbx pull actions
  
  # Pull actions matching a filter (several filters can be selected)
  ftbx pull actions --filters name=action_name
  ftbx pull actions --filters id=309
  ftbx pull actions --filters enabled=true
  ftbx pull actions --filters type=script
  ```
  
* push actions
  ```shell
  # Push action to an env (will be created if doesn't exist)
  ftbx push actions check-end-node-wf 
  ```