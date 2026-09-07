@echo off
REM FlowstateAI n8n Service Wrapper
REM This is called by NSSM to run n8n as a Windows service

REM Point n8n at the Admin user's home directory (n8n appends .n8n automatically)
set N8N_USER_FOLDER=C:\Users\Admin

REM Allow crypto and other built-in Node.js modules in n8n Code nodes
set NODE_FUNCTION_ALLOW_BUILTIN=crypto,fs,path

REM Disable analytics
set N8N_DIAGNOSTICS_ENABLED=false

"C:\Users\Admin\AppData\Roaming\npm\n8n.cmd"
