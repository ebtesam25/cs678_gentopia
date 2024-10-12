### Define your custom tool here. Check prebuilts in gentopia.tool (:###
from gentopia.tools import *
import re
import os

class HtmlSaver:
    def __init__(self, filename="pitch_deck.html"):
        self.filename = filename

    def save_html(self, html_code):
        # Remove leading and trailing whitespace (including newlines)
        # Using regex, get html code between <!DOCTYPE html> and </html> tags
        html_code = re.search(r'<!DOCTYPE html>(.*?)</html>', html_code, re.DOTALL).group(1)
        html_code = html_code.strip()

        # Write the HTML code to the specified file
        with open(self.filename, 'w') as f:
            f.write(html_code)
        
        return f"HTML code saved to {self.filename}"

class HtmlSaverTool(BaseTool):
    """HTML Saver Tool"""
    name = "html_saver"
    description = "A tool to save HTML code to a file named 'pitch_deck_(timestamp).html'. Input should be valid HTML code."
    args_schema: Optional[Type[BaseModel]] = create_model("HtmlSaver", html_code=(str, ...))
    saver = HtmlSaver()

    def _run(self, html_code: AnyStr) -> Any:
        return self.saver.save_html(html_code)

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

if __name__ == "__main__":
    tool = HtmlSaverTool()
    html_code = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LLM Evaluation Pitch Deck</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.4.0/reveal.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.4.0/theme/black.css" id="theme">
    <style>
        /* Custom styles (optional) */
        .reveal section {
            font-size: 1.5em;
            text-align: center;
        }
    </style>
</head>
<body>

<div class="reveal">
    <div class="slides">
        <section>
            <h2>Evaluation of Large Language Models (LLMs)</h2>
            <h4>Metrics, Techniques, and Challenges</h4>
            <p>Introductory slide to set the stage for LLM evaluation.</p>
        </section>
        <section>
            <h2>Why Evaluate LLMs?</h2>
            <p>Discuss the necessity of LLM evaluation and its impact on real-world applications.</p>
        </section>
        <section>
            <h2>Types of Evaluation</h2>
            <p>Overview of intrinsic, extrinsic, and human evaluations.</p>
        </section>
        <section>
            <h2>Intrinsic Metrics for LLMs</h2>
            <p>Key metrics like perplexity, accuracy, log likelihood.</p>
        </section>
        <section>
            <h2>Extrinsic Evaluation: Use Case Testing</h2>
            <p>Evaluating models based on task-specific performance.</p>
        </section>
        <section>
            <h2>Human Evaluation</h2>
            <p>Qualitative judgment from humans, including coherence and fluency.</p>
        </section>
        <section>
            <h2>Challenges in LLM Evaluation</h2>
            <p>Explore ongoing challenges such as robustness, scalability, and fairness.</p>
        </section>
    </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.4.0/reveal.min.js"></script>
<script>
    // Initialize Reveal.js
    Reveal.initialize({
        hash: true,
        transition: 'slide', // none/fade/slide/convex/concave/zoom
    });
</script>

</body>
</html>

    """
    result = tool._run(html_code)
    print(result)

    
