import boto3
from pprint import pprint
import csv

def get_eip_info_region(region_name) :
    '''
    Return a list of CSV records one for each AWS Region
    :param region_name:
    :return:
    '''

    csv_list = []
    csv_rec  = {}

    client = boto3.client('ec2',region_name)
    addresses_dict = client.describe_addresses()

    print ("==============================================")
    pprint(addresses_dict)

    for eip_dict in addresses_dict['Addresses']:
        print ("+++++++++++++++++++++")
        pprint(eip_dict)
        flag_up = ""

        if eip_dict.has_key('AssociationId') == False :
            associationId = "UNASSOCIATED"
        else:
            associationId = eip_dict['AssociationId']

        if eip_dict.has_key('Tags') == True :
            tags = "yes"
        else:
            tags = "NO"
            flag_up += "*"

        if eip_dict.has_key('PrivateIpAddress') == True :
            private_ip = eip_dict['PrivateIpAddress']
        else:
            private_ip = "None"

        # Flag up to the report reader
        # * ->  EIP is not tagged
        # ! -> EIP is not associated
        if associationId == "UNASSOCIATED" :
            flag_up += "!"

        # Print out info if this region had at least one EIP
        if len(addresses_dict['Addresses']) > 0:
            csv_rec['AWS Region'] = region
            csv_rec['Private IP'] = private_ip
            csv_rec['EIP'] = eip_dict['PublicIp']
            csv_rec['Domain'] = eip_dict['Domain']
            csv_rec['EIP Allocation Id'] = eip_dict['AllocationId']
            csv_rec['EIP Association Id'] = associationId
            csv_rec['Tagged'] = tags
            csv_rec['Attention'] = flag_up

            #print("A CSV rec looks like :")
            #pprint(csv_rec)

            csv_list.append(csv_rec)

        else : # No EIP addresses returned from AWS
            csv_rec = None

    #print "CSV recs ::-"
    #pprint(csv_list)

    return csv_list


if __name__ == '__main__' :
    output_filename = 'eip_compliance_report.csv'

    print 'Started...'

    all_csv_recs = []   # This is a list of dictionaries - each dictionary is a row for the CSV file

    region_list = ['us-east-1','us-east-2','eu-west-1','eu-west-2','ap-south-1','ap-south-1','ap-northeast-1','ap-northeast-2','ap-southeast-1','ap-southeast-2','ca-central-1','eu-central-1','eu-west-1','eu-west-2','eu-west-3']
    for region in region_list :
        csv_list = get_eip_info_region(region)
        if len(csv_list) > 0:
            #print csv_list
            for i in csv_list:
                all_csv_recs.append(i)

    #print "============================================="
    #print "All data to be written for CSV all_csv_recs[]"
    #print "============================================="

    # This should be a list of dictionaries
    #pprint(all_csv_recs)

    # Write results out to a CSV file

    with open(output_filename, 'w') as csvfile:

        # Need headers in the file to promote self-documentation
        fieldnames = ['AWS Region', 'Private IP', 'EIP', 'Domain', 'EIP Allocation Id', 'EIP Association Id', 'Tagged', 'Attention']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for rec in all_csv_recs:
            writer.writerow({'AWS Region'           : rec['AWS Region'],
                             'Private IP'           : rec['Private IP'],
                             'EIP'                  : rec['EIP'],
                             'Domain'               : rec['Domain'],
                             'EIP Allocation Id'    : rec['EIP Allocation Id'],
                             'EIP Association Id'   : rec['EIP Association Id'],
                             'Tagged'               : rec['Tagged'],
                             'Attention'            : rec['Attention']
                             })
    print "\n\n"
    print 'Finished OK, report is stored in : ' + output_filename