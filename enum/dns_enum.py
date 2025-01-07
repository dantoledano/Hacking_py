import dns.resolver

target_domain = 'youtube.com'
records_type = ['A', 'AAAA', 'CNAME', 'MX', 'TXT', 'SOA']

resolver = dns.resolver.Resolver() # Create a new instance of the resolver

for record_type in records_type: # Loop through records 
    try:
        answer = resolver.resolve(target_domain,record_type) # Get answer
    except dns.resolver.NoAnswer:
        continue
    print(f'{record_type} records for {target_domain}:')
    for data in answer:
        print(f'{data}')