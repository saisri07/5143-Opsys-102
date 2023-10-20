#!/usr/bin/env python
import subprocess
 

    
def history(**kwargs):
    result=""
    for x in kwargs:
        if(result!=""):
            result+="/n"
        result+=x
    return result
