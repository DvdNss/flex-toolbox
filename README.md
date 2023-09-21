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

  # List assets with fql
  ftbx list assets --filters "fql=(mimetype~mp4)"
  
  # List 5 jobs in a failed status
  ftbx list jobs --filters status=Failed limit=5
  ```
  > available items are: ['accounts', 'actions', 'assets', 'collections', 'eventHandlers', 'events', 'groups', 'jobs',
              'messageTemplates', 'metadataDefinitions', 'objectTypes', 'profiles', 'quotas', 'resources', 'roles',
              'tagCollections', 'taskDefinitions', 'tasks', 'taxonomies', 'taxonomies', 'timedActions',
              'userDefinedObjectTypes', 'users', 'variants', 'variants', 'wizards', 'workflowDefinitions', 'workflows',
              'workspaces']

* pull items
  ```shell
  # Pull **ALL** actions
  ftbx pull actions
  
  # Pull actions matching a filter (several filters can be selected)
  ftbx pull actions --filters name=action_name
  ftbx pull actions --filters id=309
  ftbx pull actions --filters enabled=true
  ftbx pull actions --filters type=script
  ftbx pull actions --filters type=script enabled=true
  ```
  
* push items
  ```shell
  # Push action to an env (will be created if doesn't exist)
  ftbx push actions check-end-node-wf 
  ```