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
output hostname string = site.properties.defaultHostname
