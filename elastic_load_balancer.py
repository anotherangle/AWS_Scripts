import boto3
import json

def instance_info(instance_id,i):
    ec2 = boto3.client('ec2')
    instance = ec2.describe_instances(InstanceIds=[instance_id,],)
    for tag in instance["Reservations"][0]["Instances"][0]["Tags"]:
        if tag["Key"] == "Name":
            print str(i)+"\t"+tag["Value"]+"\t"+instance_id

def old_elb_info(elb_name):
    global client
    client = boto3.client('elb')
    response = client.describe_load_balancers(
    LoadBalancerNames=[elb_name,],)
    #print response['LoadBalancerDescriptions'][0]['Instances']
    #print "________________________________________"
    this_data = response['LoadBalancerDescriptions'][0]
    global instances
    instances=[]
    i=0
    #print this_data
    for uid in this_data['Instances']:
        instances.append(str(uid['InstanceId']))
        instance_info(uid['InstanceId'],i)
        i=i+1

def registration(instance_list,old_elb,new_elb):
    for i in instance_list:
        print instances[i]
        deregister = client.deregister_instances_from_load_balancer(LoadBalancerName=old_elb,Instances=[{'InstanceId': instances[i]},])
        register = client.register_instances_with_load_balancer(LoadBalancerName=new_elb,Instances=[{'InstanceId': instances[i]},])

elb1_name = raw_input("Enter 1st ELB name:-   ")
elb2_name = raw_input("Enter 2nd ELB name:-   ")
old_elb_info(elb1_name)
instance_list=raw_input('Enter the instance number seprated by space')
numbers = map(int, instance_list.split())
#print numbers
registration(numbers,elb1_name,elb2_name)
