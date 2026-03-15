require 'sinatra'
require 'telegram/bot'
require 'json'
require 'dotenv/load'

token = ENV['BOT_TOKEN']
set :port, ENV['PORT'] || 3000
set :bind, '0.0.0.0'

post '/webhook' do
  updates = JSON.parse(request.body.read)['result']
  updates.each { |u| process_message(u) }
  status 200
end

def process_message(update)
  return unless update['message']
  
  chat_id = update['message']['chat']['id']
  text = update['message']['text']
  
  case text
  when '/start'
    Telegram::Bot::Client.new(token).api.send_message(
      chat_id: chat_id,
      text: "🚀 *FastRB v5.0 SUPER BOT*\n\n📱 *4 Platforma:*\n✅ YouTube\n✅ TikTok\n✅ Instagram\n✅ Facebook\n\n💎 FREE 5 video/oy\n💰 PRO Unlimited\n\n*Link yuboring!*",
      parse_mode: 'Markdown'
    )
  when '/premium'
    Telegram::Bot::Client.new(token).api.send_message(chat_id: chat_id, text: "💎 PRO $9/oy\nStripe: stripe.com/pay")
  when /\Ahttp/
    download_all_platforms(chat_id, text)
  end
end

def download_all_platforms(chat_id, url)
  Telegram::Bot::Client.new(token).api.send_message(chat_id: chat_id, text: "⚡ Video tayyorlanmoqda...")
  
  video_url = case url
  when /youtube/i; "https://www.y2mate.com/youtube/#{url.gsub('https://www.youtube.com/watch?v=','')}"
  when /tiktok/i; "https://tikwm.com/api/?url=#{url}"
  when /instagram/i; "https://igram.world/api/#{url}"
  when /facebook/i; "https://fdown.net/download.php?url=#{url}"
  end
  
  Telegram::Bot::Client.new(token).api.send_video(
    chat_id: chat_id,
    video: video_url,
    caption: "✨ *FastRB SUPER!*\n\n➕ /premium"
  )
end

puts "🚀 FastRB v5.0 LIVE on #{settings.port}!"
run Sinatra::Application
