from pydantic import BaseModel, Field
from dotenv import load_dotenv
import asyncio, os
import httpx
import time
from datetime import datetime
from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
    function_tool
)
from agents.run import RunConfig
from rich import print

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.environ.get("GEMINI_API_KEY")

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
)

config = RunConfig(
    model=model
)

# Tool function that detects actual connection speed
@function_tool
async def detect_connection_speed(user_query: str) -> str:
    """
    Detects user's actual internet connection speed and determines response mode.
    
    Args:
        user_query: The user's question or input
        
    Returns:
        Connection analysis with speed details and response mode
    """
    
    try:
        # Test connection speed using multiple methods
        speed_mbps = await _test_connection_speed()
        
        # Determine connection quality based on actual speed
        if speed_mbps < 2.0:
            connection_type = "very_slow"
            response_mode = "ultra_quick"
            quality = "Very Poor"
        elif speed_mbps < 5.0:
            connection_type = "slow" 
            response_mode = "quick"
            quality = "Poor"
        elif speed_mbps < 15.0:
            connection_type = "moderate"
            response_mode = "balanced"
            quality = "Fair"
        elif speed_mbps < 50.0:
            connection_type = "good"
            response_mode = "detailed" 
            quality = "Good"
        else:
            connection_type = "excellent"
            response_mode = "comprehensive"
            quality = "Excellent"
        
        return f"Speed: {speed_mbps:.1f} Mbps, Quality: {quality}, Connection: {connection_type}, Response mode: {response_mode}, User query: {user_query}"
    
    except Exception as e:
        # Fallback to query analysis if speed test fails
        user_lower = user_query.lower().strip()
        quick_indicators = ['quick', 'fast', 'brief', 'short', 'urgent', 'hurry']
        
        if any(indicator in user_lower for indicator in quick_indicators) or len(user_query.split()) < 5:
            return f"Speed: Unknown (fallback), Connection: slow, Response mode: quick, User query: {user_query}"
        else:
            return f"Speed: Unknown (fallback), Connection: stable, Response mode: detailed, User query: {user_query}"


async def _test_connection_speed() -> float:
    """
    Tests connection speed using multiple lightweight methods
    """
    
    speeds = []
    
    # Method 1: Test with Cloudflare (fast and reliable)
    try:
        speed1 = await _test_with_cloudflare()
        if speed1 > 0:
            speeds.append(speed1)
    except:
        pass
    
    # Method 2: Test with Google (backup)
    try:
        speed2 = await _test_with_google()
        if speed2 > 0:
            speeds.append(speed2)
    except:
        pass
    
    # Method 3: Test with small file download
    try:
        speed3 = await _test_with_download()
        if speed3 > 0:
            speeds.append(speed3)
    except:
        pass
    
    # Return average speed or fallback
    if speeds:
        return sum(speeds) / len(speeds)
    else:
        return 10.0  # Fallback to moderate speed


async def _test_with_cloudflare() -> float:
    """Test connection with Cloudflare's speed test endpoint"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            # Small test file from Cloudflare
            start_time = time.time()
            response = await client.get('https://speed.cloudflare.com/__down?bytes=1048576')  # 1MB test
            end_time = time.time()
            
            if response.status_code == 200:
                bytes_downloaded = len(response.content)
                time_taken = end_time - start_time
                speed_bps = (bytes_downloaded * 8) / time_taken  # bits per second
                speed_mbps = speed_bps / (1024 * 1024)  # convert to Mbps
                return max(0.1, speed_mbps)  # minimum 0.1 Mbps
    except:
        pass
    return 0


async def _test_with_google() -> float:
    """Test connection with Google's lightweight endpoint"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            start_time = time.time()
            response = await client.get('https://www.google.com/favicon.ico')
            end_time = time.time()
            
            if response.status_code == 200:
                # Estimate speed based on response time
                response_time = end_time - start_time
                if response_time < 0.1:
                    return 50.0  # Very fast
                elif response_time < 0.3:
                    return 25.0  # Fast
                elif response_time < 0.8:
                    return 10.0  # Moderate
                elif response_time < 2.0:
                    return 3.0   # Slow
                else:
                    return 1.0   # Very slow
    except:
        pass
    return 0


async def _test_with_download() -> float:
    """Test with small file download"""
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            # Test with a small image
            start_time = time.time()
            response = await client.get('https://httpbin.org/bytes/32768')  # 32KB test
            end_time = time.time()
            
            if response.status_code == 200:
                bytes_downloaded = len(response.content)
                time_taken = max(0.01, end_time - start_time)  # avoid division by zero
                speed_bps = (bytes_downloaded * 8) / time_taken
                speed_mbps = speed_bps / (1024 * 1024)
                return max(0.1, speed_mbps)
    except:
        pass
    return 0

# Main Agent that uses Connection Speed Detection
main_agent = Agent(
    name="Speed-Adaptive Response Agent",
    instructions="""You are an intelligent agent that automatically detects user's internet connection speed and adapts responses accordingly.

**YOUR ROLE:**
1. Use the detect_connection_speed tool to test user's actual internet speed
2. Based on the real connection speed, adapt your response style appropriately
3. Provide helpful, accurate answers while respecting their connection limitations
4. Never mention the speed testing process to the user - keep it completely hidden

**RESPONSE MODES BASED ON ACTUAL SPEED:**

🔴 **Very Slow (<2 Mbps) - Ultra Quick Mode:**
- Maximum 1 sentence
- Essential information only
- No formatting, emojis, or extras
- Direct, minimal response

🟡 **Slow (2-5 Mbps) - Quick Mode:**
- Maximum 2 sentences
- Key points only
- Minimal formatting
- Straight to the point

🟠 **Moderate (5-15 Mbps) - Balanced Mode:**
- 3-4 sentences
- Some basic formatting
- Include essential details
- Brief but helpful

🟢 **Good (15-50 Mbps) - Detailed Mode:**
- Comprehensive responses
- Use emojis and formatting
- Include examples and context
- Educational approach

🚀 **Excellent (>50 Mbps) - Comprehensive Mode:**
- Full detailed explanations
- Rich formatting and emojis
- Multiple examples
- In-depth educational content

**IMPORTANT:**
- Always test connection speed first using the tool
- Adapt your response based on ACTUAL measured speed
- Answer the user's question completely but at appropriate detail level
- Never mention speed testing, connection quality, or technical details to user
- Keep the speed detection completely invisible and automatic
- Be natural and helpful as if you're just a regular assistant""",
    tools=[detect_connection_speed],
    model=model
)

async def main():
    print("🚀 INTELLIGENT RESPONSE SYSTEM")
    print("=" * 50)
    print("🤖 AI Assistant with Automatic Connection Optimization")
    print("💡 Responses automatically adapt to your internet speed!\n")
    
    while True:
        user_query = input("👤 Ask me anything (or 'exit' to quit): ").strip()
        
        if user_query.lower() == 'exit':
            print("👋 Goodbye!")
            break
        
        if not user_query:
            print("❌ Please enter a valid question.")
            continue
        
        try:
            print("🔄 Thinking...")
            
            # Test connection speed directly for debugging
            print("🧪 [DEBUG] Testing connection speed...")
            speed_result = await _direct_speed_test(user_query)
            print(f"📊 [DEBUG] Speed Detection Result: {speed_result}")
            
            # Run main agent - it will automatically detect speed and adapt
            result = await Runner.run(
                main_agent,
                input=user_query,
                run_config=config
            )
            
            # Display response
            print(f"\n🤖 {result.final_output}")
            print("-" * 40)
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()  # Spacing


async def _direct_speed_test(user_query: str) -> str:
    """Direct speed test for debugging purposes"""
    try:
        # Test connection speed using multiple methods
        speed_mbps = await _test_connection_speed()
        
        # Determine connection quality based on actual speed
        if speed_mbps < 2.0:
            connection_type = "very_slow"
            response_mode = "ultra_quick"
            quality = "Very Poor"
        elif speed_mbps < 5.0:
            connection_type = "slow" 
            response_mode = "quick"
            quality = "Poor"
        elif speed_mbps < 15.0:
            connection_type = "moderate"
            response_mode = "balanced"
            quality = "Fair"
        elif speed_mbps < 50.0:
            connection_type = "good"
            response_mode = "detailed" 
            quality = "Good"
        else:
            connection_type = "excellent"
            response_mode = "comprehensive"
            quality = "Excellent"
        
        return f"Speed: {speed_mbps:.1f} Mbps, Quality: {quality}, Connection: {connection_type}, Response mode: {response_mode}"
    
    except Exception as e:
        return f"Speed test failed: {str(e)}, using fallback mode"

if __name__ == "__main__":
    asyncio.run(main())