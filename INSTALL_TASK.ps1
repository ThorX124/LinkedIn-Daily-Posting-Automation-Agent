# LinkedIn Daily Poster - Task Scheduler Installation
# RIGHT-CLICK this file and select "Run with PowerShell" or "Run as Administrator"

$taskName = "LinkedIn Daily Poster"
$scriptPath = "E:\Anas Stuff\SMIT\LinkedIn Automation\daily_fresh_poster.py"
$workingDir = "E:\Anas Stuff\SMIT\LinkedIn Automation"

Write-Host "Installing LinkedIn Daily Poster task..." -ForegroundColor Cyan

# Delete existing task if present
Unregister-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

# Create action
$action = New-ScheduledTaskAction -Execute "py" -Argument "-3 `"$scriptPath`" --auto" -WorkingDirectory $workingDir

# Create trigger (daily at 2 PM PKT = 9 AM UTC)
$trigger = New-ScheduledTaskTrigger -Daily -At 14:00

# Settings: wake to run, run if missed, allow on battery
$settings = New-ScheduledTaskSettingsSet -WakeToRun -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

# Create and register the task
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -RunLevel Highest -Force

# Enable wake timers in power plan
Write-Host "Enabling wake timers..." -ForegroundColor Cyan
powercfg /setacvalueindex 381b4222-f694-41f0-9685-ff5bb260df2e 238c9fa8-0aad-41ed-83f4-97be242c8f20 bd3b718a-0680-4d9d-8ab2-e1d2b4ac806d 1
powercfg /setdcvalueindex 381b4222-f694-41f0-9685-ff5bb260df2e 238c9fa8-0aad-41ed-83f4-97be242c8f20 bd3b718a-0680-4d9d-8ab2-e1d2b4ac806d 1

Write-Host ""
Write-Host "SUCCESS!" -ForegroundColor Green
Write-Host ""
Write-Host "Task: $taskName"
Write-Host "Schedule: Daily at 2:00 PM (14:00)"
Write-Host ""
Write-Host "To verify: Open Task Scheduler and find '$taskName'"
Write-Host "To test: Right-click task -> Run"
Write-Host ""
Write-Host "NOTE: If wake timers don't work, your BIOS may not support them."
Write-Host "      The task will still run when PC is on, even if wake fails."
