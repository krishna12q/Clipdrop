from Clipdrop.helpers.supabase.supabase_client import supabase

buckets = supabase.storage.list_buckets()

print(buckets)