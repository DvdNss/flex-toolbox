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
  
* query anything
  ```shell
  # GET
  ftbx query GET actions/410 # same as below
  ftbx query GET https://master.cs-sandbox.flex.cs.dalet.cloud/api/actions/410
  
  # POST/PUT
  ftbx query PUT actions/410/configuration --payload payload.json
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
              'tagCollections', 'taskDefinitions', 'tasks', 'taxonomies', 'timedActions',
              'userDefinedObjectTypes', 'users', 'variants', 'wizards', 'workflowDefinitions', 'workflows',
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
  
  # Pull **ALL**
  ftbx pull all
  ```
  
* push items
  ```shell
  # Push action to an env (will be created if doesn't exist)
  ftbx push actions check-end-node-wf 
  
  # Push job
  ftbx push jobs 294036
  
  # push action to failed jobs and retry them
  ftbx push actions check-end-node-wf --push_to_failed_jobs true
  ```
  
* restore backup (in config_item/item_name/backup)
  ```shell
  ftbx restore actions set-tech-metadata-dpx "2023-10-10 15h53m43s"
  ```