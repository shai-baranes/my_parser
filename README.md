

## Sniffing online changing files in Linux/Unix:

> tailf /logfile.log | grep -E "string to capture"


## Sniffing online changing files in Windows equivalent:
> note that it works only under windows power-shall and not under the basic command prompt ('CTRL+C' to abort)

- simple find (captures the entire line):
> Get-Content logfile.log -Wait | Select-String "string to capture"

- regex supported find:
> Get-Content logfile.log -Wait | Select-String -Pattern "your regex here"
