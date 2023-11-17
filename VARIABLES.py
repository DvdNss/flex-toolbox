"""

    PROJECT: flex_toolbox
    FILENAME: VARIABLES.py
    AUTHOR: David NAISSE
    DATE: September 11, 2023

    DESCRIPTION: variables file

"""
# PATHS
ENV_FILE_PATH = "C:\\Users\\dvdna\\PycharmProjects\\flex_toolbox\\environments.json"

# DEFAULT CONFIGS
ACTION_CONFIG = {
    "accountId": 0,
    "allowedAutoRetryAttempts": "",
    "autoRetryInterval": "",
    "concurrentJobsLimit": 0,
    "description": "",
    # "externalIds": [
    #     {}
    # ],
    "name": "",
    "pluginClass": "",
    "pluginUuid": "",
    "priority": "",
    # "redoActionId": -1,
    "runRuleExpression": "",
    "supportsAutoRetry": False,
    "timeout": 0,
    "type": "",
    # "undoActionId": -1,
    "useLatestAvailableVersion": True,
    "visibilityIds": [
        0
    ]
}

WORKFLOW_CONFIG = {
    "accountId": 0,
    "concurrentWorkflowLimit": 0,
    "description": "string",
    "name": "string",
    "visibilityIds": [
        0
    ]
}

DEFAULT_GROOVY_SCRIPT = "import com.ooyala.flex.plugins.PluginCommand\n\nclass script extends PluginCommand {\n\tdef execute(){\n\t\t// your code here\n\t}\n}"

# COMMANDS CONFIG ITEMS
FLEX_ITEMS_PULL = ['all', 'accounts', 'actions', 'assets', 'collections', 'eventHandlers', 'events', 'groups', 'jobs',
                   'messageTemplates', 'metadataDefinitions', 'objectTypes', 'profiles', 'quotas', 'resources', 'roles',
                   'tagCollections', 'taskDefinitions', 'tasks', 'taxonomies', 'timedActions',
                   'userDefinedObjectTypes', 'users', 'variants', 'wizards', 'workflowDefinitions',
                   'workflows', 'workspaces']

FLEX_ITEMS_LIST = ['accounts', 'actions', 'assets', 'collections', 'eventHandlers', 'events', 'groups', 'jobs',
                   'messageTemplates', 'metadataDefinitions', 'objectTypes', 'profiles', 'quotas', 'resources', 'roles',
                   'tagCollections', 'taskDefinitions', 'tasks', 'taxonomies', 'timedActions', 'userDefinedObjectTypes',
                   'users', 'variants', 'wizards', 'workflowDefinitions', 'workflows', 'workspaces']

FLEX_ITEMS_PUSH = ['accounts', 'actions', 'assets', 'collections', 'eventHandlers', 'events', 'groups', 'jobs',
                   'messageTemplates', 'metadataDefinitions', 'objectTypes', 'profiles', 'quotas', 'resources', 'roles',
                   'tagCollections', 'taskDefinitions', 'tasks', 'taxonomies', 'timedActions', 'userDefinedObjectTypes',
                   'users', 'variants', 'wizards', 'workflowDefinitions', 'workflows', 'workspaces']

FLEX_ITEMS_RESTORE = ['accounts', 'actions', 'assets', 'collections', 'eventHandlers', 'events', 'groups', 'jobs',
                      'messageTemplates', 'metadataDefinitions', 'objectTypes', 'profiles', 'quotas', 'resources',
                      'roles', 'tagCollections', 'taskDefinitions', 'tasks', 'taxonomies', 'timedActions',
                      'userDefinedObjectTypes', 'users', 'variants', 'wizards', 'workflowDefinitions', 'workflows',
                      'workspaces']

FLEX_ITEMS_COMPARE = ['accounts', 'actions', 'eventHandlers', 'groups', 'messageTemplates', 'metadataDefinitions',
                      'objectTypes', 'profiles', 'quotas', 'resources', 'roles', 'tagCollections', 'taskDefinitions',
                      'taxonomies', 'timedActions', 'userDefinedObjectTypes', 'users', 'variants', 'wizards',
                      'workflowDefinitions', 'workspaces']

# CONFIG ITEMS SUB ITEMS
ACCOUNTS_SUB_ITEMS = ['metadata', 'properties']
ACTIONS_SUB_ITEMS = ['configuration']
ASSETS_SUB_ITEMS = ['metadata']
COLLECTIONS_SUB_ITEMS = ['metadata']
EVENT_HANDLERS_SUB_ITEMS = ['configuration']
EVENTS_SUB_ITEMS = []
GROUPS_SUB_ITEMS = ['members']
JOBS_SUB_ITEMS = ['configuration', 'history']
MESSAGE_TEMPLATES_SUB_ITEMS = ['body']
METADATA_DEFINITIONS_SUB_ITEMS = ['definition']
OBJECT_TYPES_SUB_ITEMS = []
PROFILES_SUB_ITEMS = ['configuration']
QUOTAS_SUB_ITEMS = []
RESOURCES_SUB_ITEMS = ['configuration']
ROLES_SUB_ITEMS = []
TAG_COLLECTIONS_SUB_ITEMS = []
TASK_DEFINITIONS_SUB_ITEMS = []
TASKS_SUB_ITEMS = []
TAXONOMIES_SUB_ITEMS = []
TIMED_ACTIONS_SUB_ITEMS = ['configuration']
USER_DEFINED_OBJECT_TYPES_SUB_ITEMS = ['hierarchy', 'relationships']
USERS_SUB_ITEMS = []
VARIANTS_SUB_ITEMS = []
WIZARDS_SUB_ITEMS = ['configuration']
WORKFLOW_DEFINITIONS_SUB_ITEMS = ['structure']
WORKFLOWS_SUB_ITEMS = ['jobs']
WORKSPACES_SUB_ITEMS = []
