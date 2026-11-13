from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Setup the folder where our HTML file lives
templates = Jinja2Templates(directory="templates")

# --- Your LeetCode Logic ---
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        seen = {}
        for index, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], index]
            seen[num] = index
        return []

solver = Solution()

# --- 1. Display the HTML Page (GET Request) ---
@app.get("/", response_class=HTMLResponse)
def read_form(request: Request):
    # Change this line to use context=
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={"request": request}
    )

@app.post("/", response_class=HTMLResponse)
def handle_form(
    request: Request, 
    nums: str = Form(...),    
    target: int = Form(...)   
):
    result = ""
    explanation = ""
    error = ""
    
    try:
        nums_list = [int(x.strip()) for x in nums.replace(',', ' ').split() if x.strip()]
        if len(nums_list) < 2:
            error = "Please enter at least two numbers."
        else:
            ans = solver.twoSum(nums_list, target)
            if ans:
                result = f"Indices found: {ans}"
                # FIXED HERE: We now explicitly grab index 0 and index 1 out of 'ans'
                explanation = f"Because nums[{ans[0]}] + nums[{ans[1]}] ➔ {nums_list[ans[0]]} + {nums_list[ans[1]]} = {target}"
            else:
                result = "No pair matches the target sum."
                
    except ValueError:
        error = "Invalid input! Please enter only integers (e.g., 7, 9, 2, 6)."

    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={"request": request, "result": result, "explanation": explanation, "error": error}
    )
       
# This replaces app.run() from Flask
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
