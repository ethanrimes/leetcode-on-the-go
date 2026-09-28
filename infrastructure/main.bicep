param name string = 'leetcode-on-the-go'
param location string = 'westus2'

resource site 'Microsoft.Web/staticSites@2023-12-01' = {
  name: name
  location: location
  sku: { name: 'Free', tier: 'Free' }
  tags: { project: 'leetcode-on-the-go', managedBy: 'repository' }
  properties: {
    stagingEnvironmentPolicy: 'Enabled'
    allowConfigFileUpdates: true
  }
}

resource storage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: 'patlas${uniqueString(resourceGroup().id)}'
  location: location
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
  tags: { project: 'leetcode-on-the-go', managedBy: 'repository' }
  properties: {
    supportsHttpsTrafficOnly: true
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    publicNetworkAccess: 'Enabled'
  }
}

resource tableService 'Microsoft.Storage/storageAccounts/tableServices@2023-05-01' = {
  parent: storage
  name: 'default'
}

resource historyTable 'Microsoft.Storage/storageAccounts/tableServices/tables@2023-05-01' = {
  parent: tableService
  name: 'PatternAtlasHistory'
}

output hostname string = site.properties.defaultHostname
output storageName string = storage.name
