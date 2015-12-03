import requests
import json


msm_meta_cache = {}
msm_results = {}

def msm_meta_fetch(m_id):   
    print 'Fetching measurement metadata'
    try:
       url = "https://atlas.ripe.net/api/v1/measurement/%s/" % (m_id)
       response = requests.get( url )
       my_dict  = json.loads(response.text)
       msm_meta_cache[ m_id ] = my_dict
    except:
       pass


def get_all_anchor_measurements():
    print 'Getting anchor measurements'
    response_list = []
    start_url = 'https://atlas.ripe.net/api/v2/anchor-measurements/?format=json'
    
    response = requests.get(start_url)
    my_dict = json.loads(response.text)
    
    url = my_dict['next']
    
    while url != None:
        response = requests.get(url)
        my_dict = json.loads(response.text)
        url = my_dict['next']
        response_list.append(my_dict['results'])
        
    return response_list

def get_latest_measurements(m_id,num_results):
            url = 'https://atlas.ripe.net/api/v1/measurement-latest/%s/?versions=%s' %(m_id,num_results)
            response = requests.get(url)
            result = json.loads(response.text)
            return result


def get_msm_results(id, num_results):
    #merge with above, no idea why two functions
    msm_results = {}
    result = get_latest_measurements(id, 10)
    msm_results[id] = result
    return msm_results 


def get_msm_ids(dst_name):
    test_list = []
    for k,v in msm_meta_cache.iteritems():
        if dst_name in v['dst_name']:
            test_list.append(k)
    return test_list
        
def show_available_measurements():
    try:
        print 'Available IPv4 measurements'
        
        for id in ids:
            if 'IPv4' in msm_meta_cache[id]['description']:
                print msm_meta_cache[id]['description'], msm_meta_cache[id]['type']['name']
        print 
        
        print 'Available IPv6 measurements'
        for id in ids:
            if 'IPv6' in msm_meta_cache[id]['description']:
                print msm_meta_cache[id]['description'], msm_meta_cache[id]['type']['name']
        print 
    except:
        print 'Sorry - have you queried the measurment results'



def get_anchor_measurments_and_meta():
    # get all anchor measurements and metadata about the measurments
    responses = get_all_anchor_measurements()
    
    for list in responses:
        for response in list:
            msm_meta_fetch(str(response['measurement']))


# get all anchor measurements and metadata about the measurments
get_anchor_measurments_and_meta()


# SELECT AN ANCHOR
# NZRS 
# Probe ID '1042408'
# dst_name: nz-lyj-as17746

dst_name = 'nz-lyj-as17746'
ids = get_msm_ids(dst_name)

msm_results_list = []
for id in ids:
    results = get_msm_results(id, 10)
    msm_results_list.append(results)
    
# Show available tests

print show_available_measurements()
        
        
# find all ipv6 measurements and discard non IPv6

# Find IPv6 specific measurements 

ipv6_measurements = []
    
for id in ids:
    if 'IPv6' in msm_meta_cache[id]['description']:
        if msm_meta_cache[id]['msm_id'] not in ipv6_measurements:
            ipv6_measurements.append(msm_meta_cache[id]['msm_id'])

# Find probes that don't do v6 and discard

v6_probes = []

for dic in msm_results_list:
    for measurement, output in dic.iteritems(): 
        for probe, results in output.iteritems():
            for result in results:
                if result['msm_id'] in ipv6_measurements:
                    if probe not in v6_probes:
                        v6_probes.append(probe)
            
for dic in msm_results_list:
    for measurement, output in dic.iteritems(): 
        for probe, results in output.iteritems():
            if probe not in v6_probes:
                del(probe)

outer_dict = {}
test = 'http'
# Get latency
for dic in msm_results_list:
    for measurement, output in dic.iteritems():
        for probe, results in output.iteritems():
            for dic in results:
                if dic['type'] == test:
                    try:
                        inner_dict = {}
                        inner_dict['af'] = dic['result'][0]['af']
                        inner_dict['prb_id'] = dic['prb_id']
                        inner_dict['rt'] = dic['result'][0]['rt']
                        outer_dict['prb_id'] = inner_dict
                    except:
                        continue

        
            

                if result['type'] == 'http':
                    new_dict['probe'] = result
