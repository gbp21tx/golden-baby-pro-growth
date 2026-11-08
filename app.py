import os, sqlite3, csv, io, datetime, urllib.parse
import streamlit as st
st.set_page_config(page_title='Golden Baby Pro | AI Growth Bot',page_icon='🎵',layout='wide')
DB='campaign.db'
con=sqlite3.connect(DB,check_same_thread=False)
con.execute('CREATE TABLE IF NOT EXISTS campaigns (date TEXT, song TEXT, platform TEXT, impressions INTEGER, clicks INTEGER, listeners INTEGER, streams INTEGER, followers INTEGER)')
con.commit()
SONGS=['Shine Regardless','Live & Direct','Grindin’ Daily','All Around the World','Gametime','Much Throwder','Righteous King Vision','Back Against the Wall','Salute','Yung, Fly, and Flashy','Forever','Razzle Dazzle','Heaven 2 Me','I Like']
PLATFORMS=['TikTok','Instagram Reels','Facebook','YouTube Shorts']
st.title('🎵 Golden Baby Pro — AI Growth Bot')
st.caption('Legitimate audience growth • Content planning • Playlist pitches • Campaign tracking')
st.warning('This tool does not automate Spotify plays, fake engagement, mass DMs, or playlist placement. Use only permission-based outreach.')
with st.sidebar:
 st.header('Campaign setup')
 spotify=st.text_input('Official Spotify artist URL',value='https://open.spotify.com/artist/65MKFTLOAXsO7LKw09sMPh')
 audience=st.text_input('Audience / genre',value='Independent hip-hop listeners')
 tone=st.selectbox('Voice',['Confident and authentic','Inspirational','Energetic','Storytelling'])
 song=st.selectbox('Featured track',SONGS)
 link=spotify if spotify.startswith('https://open.spotify.com/') else '[insert official Spotify link]'
tabs=st.tabs(['Dashboard','Content Studio','Playlist Outreach','Campaign Tracker'])
with tabs[0]:
 st.subheader('Baseline and 90-day goals')
 a,b,c=st.columns(3)
 a.metric('Weekly listeners','4','Goal: 250');b.metric('Weekly streams','4','Goal: 500');c.metric('Followers','92','Goal: 250')
 st.markdown('**Suggested weekly routine:** Publish 4–7 short videos, test 2 hooks per featured song, engage with genuine comments, and send 5 carefully researched curator pitches.')
with tabs[1]:
 st.subheader('Generate a promotional post')
 platform=st.selectbox('Platform',PLATFORMS)
 hook=st.selectbox('Creative angle',['Behind the lyrics','Performance clip','Artist story','Question for fans','New listener introduction'])
 prompt=f'''You are the ethical music-marketing assistant for Golden Baby Pro. Write ONE {platform} promotional post for the song {song}. Target: {audience}. Tone: {tone}. Angle: {hook}. Include a short hook, 15-second video concept, caption, 3 relevant hashtags, and a gentle CTA linking to {link}. No fake claims, invented achievements, or guarantees. Avoid spam.'''
 st.code(prompt,language='text')
 st.caption('Copy this prompt into your preferred AI assistant, or add an API key below to generate directly.')
 key=st.text_input('Optional OpenAI API key',type='password',value=os.environ.get('OPENAI_API_KEY',''))
 if st.button('Generate post with AI'):
  if not key: st.info('Enter an API key to generate directly, or copy the prompt above.')
  else:
   try:
    from openai import OpenAI
    result=OpenAI(api_key=key).responses.create(model='gpt-4.1-mini',input=prompt)
    st.write(result.output_text)
   except Exception as e: st.error(f'Generation unavailable: {e}')
with tabs[2]:
 st.subheader('Personalized curator outreach')
 curator=st.text_input('Curator / playlist name')
 why=st.text_area('Why the track fits this playlist (verify manually)')
 if st.button('Draft curator pitch'):
  if not curator or not why: st.error('Add the playlist name and specific fit before drafting.')
  else:
   st.text_area('Pitch',f'Hi {curator},\n\nI’m reaching out on behalf of Golden Baby Pro. I think “{song}” could be a fit for your playlist because {why.strip()}\n\nHere is the official Spotify link: {link}\n\nThanks for considering it. No pressure either way!\n\nGolden Baby Pro team',height=210)
 st.caption('Only contact curators who accept submissions. Never pay for guaranteed streams.')
with tabs[3]:
 st.subheader('Record real campaign results')
 with st.form('entry'):
  day=st.date_input('Date',datetime.date.today());p=st.selectbox('Channel',PLATFORMS,key='trackplatform');s=st.selectbox('Track',SONGS,key='tracksong')
  a,b,c,d,e=st.columns(5)
  impressions=a.number_input('Impressions',min_value=0,step=1);clicks=b.number_input('Link clicks',min_value=0,step=1);listeners=c.number_input('Listeners',min_value=0,step=1);streams=d.number_input('Streams',min_value=0,step=1);followers=e.number_input('New followers',min_value=0,step=1)
  if st.form_submit_button('Save results'):
   con.execute('INSERT INTO campaigns VALUES (?,?,?,?,?,?,?,?)',(str(day),s,p,impressions,clicks,listeners,streams,followers));con.commit();st.success('Saved')
 rows=con.execute('SELECT * FROM campaigns ORDER BY date DESC').fetchall()
 if rows:
  headers=['Date','Song','Platform','Impressions','Clicks','Listeners','Streams','New followers']
  st.dataframe([dict(zip(headers,r)) for r in rows],use_container_width=True)
  output=io.StringIO();w=csv.writer(output);w.writerow(headers);w.writerows(rows)
  st.download_button('Export CSV',output.getvalue(),'golden_baby_pro_campaigns.csv','text/csv')
 else:st.info('Add your first campaign results to start measuring growth.')
