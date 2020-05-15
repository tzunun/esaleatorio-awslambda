# esaleatorio-awslambda
The intent I have with this repo is to generate a new site everyday.
In other words have new content everyday for the esaleatorio.com website. 
The ultimate goal is for this code to create the new posts and commit the code, this will trigger the build
and deployment of the new content.

**Python deployment package for AWS Lambda**

I found most of the instructions at
https://docs.aws.amazon.com/lambda/latest/dg/python-package.html

there are some minor tweaks, but nothing major.
The instructions assume you are in the directory where your code resides. You may need to use pip3, I used pip because I mostly use the Anaconda Distribution of Python.

```console
antonio@workstation:~$ pip install --target ./package -r requirements.txt

antonio@workstation:~$ cd package/

antonio@workstation:~$ zip -r9 ${OLDPWD}/function.zip

antonio@workstation:~$ cd $OLDPWD

antonio@workstation:~$ zip -g function.zip ./*.py 
```

These are most of the commands, the command to update the function code is not here because I have not set up AWS CLI on this partition yet. 