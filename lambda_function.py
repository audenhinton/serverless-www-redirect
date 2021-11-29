import json
import re

def lambda_handler(event, context):

    # parse request body from CloudFront
    request = event["Records"][0]["cf"]["request"]
    
    # get our host and uri parameters
    host = request["headers"]["host"][0]["value"]
    uri = request["uri"]
    
    # set empty response body
    response = {}
    
    # if the domain is from CloudFront, let's output the event body,
    # if it's not from CloudFront let's append www. to the host and
    # set the redirect
    
    if re.search(r'(cloudfront|\.cf)\.net', host):
        
        # this request is coming from CloudFront, let's return the event body for testing
        response["status"] = '200'
        response["statusDescription"] = "Success"
        response["headers"] = {
            'content-type': [{
                'key': 'Content-Type',
                'value': 'application/json'
            }]
        }
        response["body"] = json.dumps(event) 
        
    else:
        
        # this request is coming from a custom domain, let's prepend www to the front 
        # of it (and https) and append the original request uri to the end
        
        if not re.search(r'^www\.', host):
            host = "www." + host
            
        # uncomment the line below if you want to redirect users to non-www
        #host = host.replace("www.", "")
        
        # let's also set a 301 redirect in the response
        response["status"] = '301'
        response["statusDescription"] = "Found"
        response["headers"] = {
            'location': [{
                'key': 'Location',
                'value': 'https://' + host + uri
            }]
        }

    # return the response back to CloudFront
    return response
