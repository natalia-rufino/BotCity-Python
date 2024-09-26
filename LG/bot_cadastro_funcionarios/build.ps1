$exclude = @("venv", "bot_cadastro_funcionarios.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "bot_cadastro_funcionarios.zip" -Force