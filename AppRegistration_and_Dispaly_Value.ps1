# Prompt for Directory (Tenant) ID
$tenantId = Read-Host "Enter your Azure Directory (Tenant) ID"

#
$grapid = "00000003-0000-0000-c000-000000000000"
$o365id = "c5393580-f805-4401-95e8-94b7a6ef2fc2"
$dautditlogreadall = "e4c9e354-4dc5-45b8-9e7c-e1393b0b1a20=Scope"
$aauditlogreadall = "b0afded3-3588-46d8-8b3d-9842eff778da=Role"
$ddirectoryreadall = "06da0dbc-49e2-44d2-8312-53f166ab848a=Scope"
$adirectoryreadall = "7ab1d382-f21e-4acd-a863-ba3e13f7da61=Role"
$asecuritactionsreadall = "5e0edab9-c148-49d0-b423-ac253e121825=Role"
$asecurityalertreadall = "472e4a4d-bb4a-4026-98d1-0b0d74cb74a5=Role"
$aseurityeventsreadall = "bf394140-e372-4bf9-a898-299cfc7564e5=Role"
$asecurityincidentreadall = "45cc0394-e837-488b-a098-1918f48d186c=Role"
$aidentityriskeventreadall = "6e472fd1-ad78-48da-a0f0-97ab2c6b769e=Role"
$duserread = "e1fe6dd8-ba31-4d61-89e7-88639da4683d=Scope"
$duserreadall = "a154be20-db9c-4678-8ab7-66f6cc099a59=Scope"
$auserreadall = "df021288-bdef-4463-88db-98f22de89214=Role"
$duserreadbasicall = "b340eb25-3456-403f-be2f-af7a0d370277=Scope"
$adevicemanagementappsreadall = "7a6ee1e7-141e-4cec-ae74-d9db155731ff=Role"
$adevicemanagementconfigurationreadall = "dc377aa6-52d8-4e23-b271-2a7ae04cedf3=Role"
$ddevicemanagementmanageddevicesreadall = "314874da-47d6-4978-88dc-cf0d37f0bb82=Scope"
$athreatindicatorsreadall = "197ee4e9-b993-4066-898f-d6aecc55125b=Role"
$adirectoryreadwriteall = "19dbc75e-c2e2-444c-a770-ec69d8559fc7=Role"
$agroupreadwriteall = "62a82d76-70ea-41e2-9197-370581804d09=Role"
$auserreadwriteall = "741f803b-c850-494e-b5df-cde7c675a1ca=Role"
$auserenabledisableaccountall = "3011c876-62b7-4ada-afa2-506cbbecc68c=Role"
$auserpasswordprofilereadwriteall = "cc117bb9-00cf-4eb8-b580-ea2a878fe8f7=Role"
$demail = "64a6cdd6-aab1-4aaf-94b8-3cc8405e90d0=Scope"
$dprofile = "14dad69e-099b-42c9-810b-d002981feec1=Scope"

#O365 permissions 
$dactivityfeed = "594c1fb6-4f81-4475-ae41-0c394909246c=Scope"
$aactivityfeed = "594c1fb6-4f81-4475-ae41-0c394909246c=Role"
$dactivityfeedreaddlp = "4807a72c-ad38-4250-94c9-4eabfe26cd55=Scope"
$aactivityfeedreaddlp = "4807a72c-ad38-4250-94c9-4eabfe26cd55=Role"
$dservicehealth = "e2cea78f-e743-4d8f-a16a-75b629a038ae=Scope"
$aservicehealth = "e2cea78f-e743-4d8f-a16a-75b629a038ae=Role"




# Connect to Azure AD
Connect-AzureAD -TenantId $tenantId

# Check if BDTest app registration exists
$appName = "GoogleSecOps"
$app = Get-AzureADApplication -Filter "DisplayName eq '$appName'"

if (-not $app) {
    Write-Host "App registration '$appName' does not exist. Creating..."
    $app = New-AzureADApplication -DisplayName $appName
    Write-Host "Created app registration with ObjectId: $($app.ObjectId)"
} else {
    Write-Host "App registration '$appName' already exists. ObjectId: $($app.ObjectId)"
}

az ad app permission add --id $app.ObjectId --api $grapid --api-permissions $dautditlogreadall
az ad app permission add --id $app.ObjectId --api $grapid --api-permissions $aauditlogreadall
az ad app permission add --id $app.ObjectId --api $grapid --api-permissions $ddirectoryreadall
az ad app permission add --id $app.ObjectId --api $grapid --api-permissions $adirectoryreadall
az ad app permission add --id $app.ObjectId --api $grapid --api-permissions $asecuritactionsreadall
az ad app permission add --id $app.ObjectId --api $grapid --api-permissions $aseurityeventsreadall
az ad app permission add --id $app.ObjectId --api $grapid --api-permissions $aseurityeventsreadall
az ad app permission add --id $app.ObjectId --api $grapid --api-permissions $duserread
az ad app permission add --id $app.ObjectId --api $grapid --api-permissions $duserreadall
az ad app permission add --id $app.ObjectId --api $grapid --api-permissions $auserreadall
az ad app permission add --id $app.ObjectId --api $grapid --api-permissions $duserreadbasicall


az ad app permission add --id $app.ObjectId --api $o365id --api-permissions $dactivityfeed
az ad app permission add --id $app.ObjectId --api $o365id --api-permissions $aactivityfeed
az ad app permission add --id $app.ObjectId --api $o365id --api-permissions $dactivityfeedreaddlp
az ad app permission add --id $app.ObjectId --api $o365id --api-permissions $aactivityfeedreaddlp
az ad app permission add --id $app.ObjectId --api $o365id --api-permissions $dservicehealth
az ad app permission add --id $app.ObjectId --api $o365id --api-permissions $aservicehealth

# Add Office 365 permissions
Write-Host "Adding Office 365 permissions..."
foreach ($permission in $o365Permissions.GetEnumerator()) {
    Write-Host "Adding permission: $($permission.Key)"
    az ad app permission add --id $app.ObjectId --api $o365ApiId --api-permissions $permission.Value
}

# Grant admin consent for all permissions
Write-Host "Granting admin consent for all permissions..."
az rest --method POST --uri "https://graph.microsoft.com/v1.0/oauth2PermissionGrants" --body "{\"clientId\":\"$($app.ObjectId)\",\"consentType\":\"AllPrincipals\",\"resourceId\":\"$graphApiId\",\"scope\":\"AuditLog.Read.All Directory.Read.All User.Read User.Read.All User.ReadBasic.All\"}"
az rest --method POST --uri "https://graph.microsoft.com/v1.0/oauth2PermissionGrants" --body "{\"clientId\":\"$($app.ObjectId)\",\"consentType\":\"AllPrincipals\",\"resourceId\":\"$o365ApiId\",\"scope\":\"ActivityFeed.Read ActivityFeed.Read.DLP ServiceHealth.Read\"}"

# Create a new client secret
$secretName = "GoogleSecOpsSecrete"
$startDate = Get-Date
$endDate = $startDate.AddDays(730)

$secret = New-AzureADApplicationPasswordCredential -ObjectId $app.ObjectId `
    -CustomKeyIdentifier $secretName `
    -StartDate $startDate `
    -EndDate $endDate

    
Write-Host "Client Secret Value: $($secret.Value)"
Write-Host "Expires On: $($secret.EndDate)"
Write-Host "`nApplication Registration Details:"
Write-Host "--------------------------------"
Write-Host "Application Name: $appName"
Write-Host "Application ID: $($app.AppId)"
Write-Host "Object ID: $($app.ObjectId)"
Write-Host "`nClient Secret Details:"
Write-Host "--------------------------------"
Write-Host "Secret Name: $secretName"
Write-Host "Secret Value: $($secret.Value)"
