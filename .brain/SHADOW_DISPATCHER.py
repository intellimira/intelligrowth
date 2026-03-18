import os, json, time

def relay_outreach():
    if not os.path.exists('.brain/leads/authorized_leads.json'):
        print(' [Error] No leads identified.')
        return

    with open('.brain/leads/authorized_leads.json', 'r') as f:
        leads_mesh = json.load(f)

    print('\n--- ⚡️ SHADOW OPERATOR: LIVE OUTREACH RELAY ACTIVATED ---')
    for asset, leads in leads_mesh.items():
        print(f'\n[RELAY] Dispatching for: {asset}')
        outreach_path = f'.brain/outputs/outreach_packages/outreach_{asset}.md'
        
        if os.path.exists(outreach_path):
            with open(outreach_path, 'r') as f:
                script = f.read()
            
            for lead in leads:
                # HARDENED DISPATCH: Handles real-world context and sources
                name = lead.get("name", "Target")
                context = lead.get("context", "Unknown Pain")
                source = lead.get("source", "Market Sentry")
                
                print(f' >> [DISPATCH READY] Target: {name} | Context: {context} | Source: {source}')
                with open('.brain/BATTLE_LOG.md', 'a') as log:
                    log.write(f'\n### [TARGET_ENGAGED] {asset}\n- Target: {name}\n- Context: {context}\n- Source: {source}\n- Timestamp: {time.time()}\n')
                time.sleep(1)


if __name__ == '__main__':
    relay_outreach()
