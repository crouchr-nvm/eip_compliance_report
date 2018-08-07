**EIP Compliance Report**

This script is used to produce a simple compliance 
report about AWS EIPs.
According to NVM policy, all AWS resources that _can_ be tagged,
_should_ be. There is a NVM AWS Resource Tagging Policy 
in Confluence. This version of the script does not check if a tag is compliant to the NVM policy.
The script uses the boto library to query the AWS API.

An EIP is compliant if it is :
* Tagged (identified by having a * character in the Attention field)
* Associated (identified by having a ! character in the Attention field)

Note : This code will report on EIPs for the AWS account from which it is run.

_Usage_

This script uses Python 2.

An example report is available in the examples directory.
 
Run using ./eip_compliance.py

The output file called _eip_compliance_report.csv_ and can be imported directly
 in Excel for further processing if necessary.
 
_Python Dependencies_
* boto3
* csv

_Enhancements_

Add the EIP's tags to the report.

