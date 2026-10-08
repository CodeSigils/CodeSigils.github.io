
<!doctype html>
<html lang="en" class="no-js">
  <head>
    
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width,initial-scale=1">
      
        <meta name="description" content="A field note on finding non-consensual AI attribution in a blog's git history, what GitHub's contributor caches hide, and the layered cleanup that cleared it.">
      
      
        <meta name="author" content="Tom Geo">
      
      
        <link rel="canonical" href="https://codesigils.github.io/AI/Agent-Work/when-an-ai-signs-your-commits/">
      
      
        <link rel="prev" href="../agent-memory-surfaces/">
      
      
        <link rel="next" href="../../Hermes/browseros-hermes-guide/">
      
      
        
      
      
      <link rel="icon" href="../../../assets/images/favicon.png">
      <meta name="generator" content="zensical-0.0.65">
    
    
      
        <title>When an AI Agent Signs Your Commits - Code Sigils</title>
      
    
    
      
        
      
      <link rel="stylesheet" href="../../../assets/stylesheets/modern/main.40d3fdbb.min.css">
      
        
          
        
        <link rel="stylesheet" href="../../../assets/stylesheets/modern/palette.812a03bb.min.css">
      
      


    
    
      
    
    
      
        
        
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Inter:300,300i,400,400i,500,500i,700,700i%7CJetbrains+Mono:400,400i,700,700i&amp;display=fallback">
        <style>:root{--md-text-font:"Inter";--md-code-font:"Jetbrains Mono"}</style>
      
    
    
      <link rel="stylesheet" href="../../../stylesheets/extra.css">
    
    <script>__md_scope=new URL("../../..",location),__md_scope.pathname.endsWith("/")||(__md_scope=new URL(__md_scope.pathname+"/",location)),__md_hash=e=>[...e].reduce(((e,t)=>(e<<5)-e+t.charCodeAt(0)),0),__md_get=(e,t=localStorage,_=__md_scope)=>JSON.parse(t.getItem(_.pathname+"."+e)),__md_set=(e,t,_=localStorage,a=__md_scope)=>{try{_.setItem(a.pathname+"."+e,JSON.stringify(t))}catch(e){}},document.documentElement.setAttribute("data-platform",navigator.platform)</script>
    
      

    
    
  
  <link rel="alternate" type="application/rss+xml" title="Code Sigils" href="../../../feed.xml">

  </head>
  
  
    
    
      
    
    
    
    
    <body dir="ltr" data-md-color-scheme="default" data-md-color-primary="indigo" data-md-color-accent="indigo">
  
    
    <input class="md-toggle" data-md-toggle="drawer" type="checkbox" id="__drawer" autocomplete="off">
    <input class="md-toggle" data-md-toggle="search" type="checkbox" id="__search" autocomplete="off">
    <label class="md-overlay" for="__drawer" aria-label="Navigation"></label>
    <div data-md-component="skip">
      
        
        <a href="#what-the-history-actually-contained" class="md-skip">
          Skip to content
        </a>
      
    </div>
    <div data-md-component="announce">
      
    </div>
    
    
      

  

<header class="md-header md-header--shadow" data-md-component="header">
  <nav class="md-header__inner md-grid" aria-label="Header">
    <a href="../../.." title="Code Sigils" class="md-header__button md-logo" aria-label="Code Sigils" data-md-component="logo">
      
  
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="lucide lucide-book-open" viewBox="0 0 24 24"><path d="M12 5v16M20.001 19A2 2 0 0 0 22 17V5a2 2 0 0 0-1.999-2L16 3.002A5 5 0 0 0 12 5a5 5 0 0 0-4-2H4a2 2 0 0 0-2 2v12a2 2 0 0 0 1.999 2H8a5 5 0 0 1 4 2 5 5 0 0 1 4-2z"/></svg>

    </a>
    <label class="md-header__button md-icon" for="__drawer" aria-label="Navigation">
      
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="lucide lucide-menu" viewBox="0 0 24 24"><path d="M4 5h16M4 12h16M4 19h16"/></svg>
    </label>
    <div class="md-header__title" data-md-component="header-title">
      <div class="md-header__ellipsis">
        <div class="md-header__topic">
          <span class="md-ellipsis">
            Code Sigils
          </span>
        </div>
        <div class="md-header__topic" data-md-component="header-topic">
          <span class="md-ellipsis">
            
              When an AI Agent Signs Your Commits
            
          </span>
        </div>
      </div>
    </div>
    
      
        <form class="md-header__option" data-md-component="palette">
  
    
    
    
    <input class="md-option" data-md-color-media="none" data-md-color-scheme="default" data-md-color-primary="indigo" data-md-color-accent="indigo"  aria-label="Switch to dark mode"  type="radio" name="__palette" id="__palette_0">
    
      <label class="md-header__button md-icon" title="Switch to dark mode" for="__palette_1" hidden>
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="lucide lucide-sun" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>
      </label>
    
  
    
    
    
    <input class="md-option" data-md-color-media="none" data-md-color-scheme="slate" data-md-color-primary="indigo" data-md-color-accent="indigo"  aria-label="Switch to light mode"  type="radio" name="__palette" id="__palette_1">
    
      <label class="md-header__button md-icon" title="Switch to light mode" for="__palette_0" hidden>
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="lucide lucide-moon" viewBox="0 0 24 24"><path d="M20.985 12.486a9 9 0 1 1-9.473-9.472c.405-.022.617.46.402.803a6 6 0 0 0 8.268 8.268c.344-.215.825-.004.803.401"/></svg>
      </label>
    
  
</form>
      
    
    
      <script>var palette=__md_get("__palette");if(palette&&palette.color){if("(prefers-color-scheme)"===palette.color.media){var media=matchMedia("(prefers-color-scheme: light)"),input=document.querySelector(media.matches?"[data-md-color-media='(prefers-color-scheme: light)']":"[data-md-color-media='(prefers-color-scheme: dark)']");palette.color.media=input.getAttribute("data-md-color-media"),palette.color.scheme=input.getAttribute("data-md-color-scheme"),palette.color.primary=input.getAttribute("data-md-color-primary"),palette.color.accent=input.getAttribute("data-md-color-accent")}for(var[key,value]of Object.entries(palette.color))document.body.setAttribute("data-md-color-"+key,value)}</script>
    
    
    
      
      
        <label class="md-header__button md-icon" for="__search" aria-label="Search">
          
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="lucide lucide-search" viewBox="0 0 24 24"><path d="m21 21-4.34-4.34"/><circle cx="11" cy="11" r="8"/></svg>
        </label>
        <div class="md-search" data-md-component="search" role="dialog" aria-label="Search">
  <button type="button" class="md-search__button">
    Search
  </button>
</div>
      
    
    <div class="md-header__source">
      
    </div>
  </nav>
  
</header>
    
    <div class="md-container" data-md-component="container">
      
      
        
          
        
      
      <main class="md-main" data-md-component="main">
        <div class="md-main__inner md-grid">
          
            
              
              <div class="md-sidebar md-sidebar--primary" data-md-component="sidebar" data-md-type="navigation" >
                <div class="md-sidebar__scrollwrap">
                  <div class="md-sidebar__inner">
                    



<nav class="md-nav md-nav--primary" aria-label="Navigation" data-md-level="0">
  <label class="md-nav__title" for="__drawer">
    <a href="../../.." title="Code Sigils" class="md-nav__button md-logo" aria-label="Code Sigils" data-md-component="logo">
      
  
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="lucide lucide-book-open" viewBox="0 0 24 24"><path d="M12 5v16M20.001 19A2 2 0 0 0 22 17V5a2 2 0 0 0-1.999-2L16 3.002A5 5 0 0 0 12 5a5 5 0 0 0-4-2H4a2 2 0 0 0-2 2v12a2 2 0 0 0 1.999 2H8a5 5 0 0 1 4 2 5 5 0 0 1 4-2z"/></svg>

    </a>
    Code Sigils
  </label>
  
  <ul class="md-nav__list" data-md-scrollfix>
    
      
      
  
  
  
  
    <li class="md-nav__item">
      <a href="../../.." class="md-nav__link">
        
  
  
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="lucide lucide-rocket" viewBox="0 0 24 24"><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09"/><path d="M9 12a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.4 22.4 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 .05 5 .05"/></svg>
  
  <span class="md-ellipsis">
    
  
  Code Sigils

    
  </span>
  
  

      </a>
    </li>
  

    
      
      
  
  
  
  
    <li class="md-nav__item">
      <a href="../../../disclaimer/" class="md-nav__link">
        
  
  
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="lucide lucide-shield-alert" viewBox="0 0 24 24"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1zM12 8v4M12 16h.01"/></svg>
  
  <span class="md-ellipsis">
    
  
  Disclaimer

    
  </span>
  
  

      </a>
    </li>
  

    
      
      
  
  
  
  
    <li class="md-nav__item">
      <a href="../../../markdown/" class="md-nav__link">
        
  
  
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="lucide lucide-file-text" viewBox="0 0 24 24"><path d="M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z"/><path d="M14 2v5a1 1 0 0 0 1 1h5M10 9H8M16 13H8M16 17H8"/></svg>
  
  <span class="md-ellipsis">
    
  
  Markdown in 5min

    
  </span>
  
  

      </a>
    </li>
  

    
      
      
  
  
    
  
  
  
    
    
    
    
      
        
        
      
    
    
      
    
    <li class="md-nav__item md-nav__item--active md-nav__item--section md-nav__item--nested">
      
        
        
        <input class="md-nav__toggle md-toggle " type="checkbox" id="__nav_4" checked>
        
          
          <label class="md-nav__link" for="__nav_4" id="__nav_4_label" tabindex="">
            
  
  
  <span class="md-ellipsis">
    
  
  AI

    
  </span>
  
  

            <span class="md-nav__icon md-icon"></span>
          </label>
        
        
          <nav class="md-nav" data-md-level="1" aria-labelledby="__nav_4_label" aria-expanded="true">
            <label class="md-nav__title" for="__nav_4">
              <span class="md-nav__icon md-icon"></span>
              
  
  AI

            </label>
            <ul class="md-nav__list" data-md-scrollfix>
              
                
                  
  
  
  
  
    <li class="md-nav__item">
      <a href="../../" class="md-nav__link">
        
  
  
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="lucide lucide-bot" viewBox="0 0 24 24"><path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2M20 14h2M15 13v2M9 13v2"/></svg>
  
  <span class="md-ellipsis">
    
  
  AI Tools

    
  </span>
  
  

      </a>
    </li>
  

                
              
                
                  
  
  
  
  
    
    
    
    
      
    
    
      
        
        
      
    
    <li class="md-nav__item md-nav__item--pruned md-nav__item--nested">
      
        
  
  
  
  
    <a href="../../Admin-Work/samba-still-relevant/" class="md-nav__link">
      
  
  
  <span class="md-ellipsis">
    
  
  Admin Work

    
  </span>
  
  

      
        <span class="md-nav__icon md-icon"></span>
      
    </a>
  

      
    </li>
  

                
              
                
                  
  
  
    
  
  
  
    
    
    
    
      
    
    
      
    
    <li class="md-nav__item md-nav__item--active md-nav__item--nested">
      
        
        
        <input class="md-nav__toggle md-toggle " type="checkbox" id="__nav_4_3" checked>
        
          
          <label class="md-nav__link" for="__nav_4_3" id="__nav_4_3_label" tabindex="0">
            
  
  
  <span class="md-ellipsis">
    
  
  Agent Work

    
  </span>
  
  

            <span class="md-nav__icon md-icon"></span>
          </label>
        
        
          <nav class="md-nav" data-md-level="2" aria-labelledby="__nav_4_3_label" aria-expanded="true">
            <label class="md-nav__title" for="__nav_4_3">
              <span class="md-nav__icon md-icon"></span>
              
  
  Agent Work

            </label>
            <ul class="md-nav__list" data-md-scrollfix>
              
                
                  
  
  
  
  
    <li class="md-nav__item">
      <a href="../agent-instruction-drift/" class="md-nav__link">
        
  
  
  <span class="md-ellipsis">
    
  
  When Agent Instructions Start to Drift

    
  </span>
  
  

      </a>
    </li>
  

                
              
                
                  
  
  
  
  
    <li class="md-nav__item">
      <a href="../agent-maintained-awesome-list/" class="md-nav__link">
        
  
  
  <span class="md-ellipsis">
    
  
  What Keeps an Awesome List Honest

    
  </span>
  
  

      </a>
    </li>
  

                
              
                
                  
  
  
  
  
    <li class="md-nav__item">
      <a href="../agent-memory-surfaces/" class="md-nav__link">
        
  
  
  <span class="md-ellipsis">
    
  
  Where an Agent's Memory Actually Lives

    
  </span>
  
  

      </a>
    </li>
  

                
              
                
                  
  
  
    
  
  
  
    <li class="md-nav__item md-nav__item--active">
      
      
      
      
      
        <label class="md-nav__link md-nav__link--active" for="__toc">
          
  
  
  <span class="md-ellipsis">
    
  
  When an AI Agent Signs Your Commits

    
  </span>
  
  

          <span class="md-nav__icon md-icon"></span>
        </label>
      
      <a href="././" class="md-nav__link md-nav__link--active">
        
  
  
  <span class="md-ellipsis">
    
  
  When an AI Agent Signs Your Commits

    
  </span>
  
  

      </a>
      
        


<nav class="md-nav md-nav--secondary" aria-label="On this page">
  
  
  
  
    <label class="md-nav__title" for="__toc">
      <span class="md-nav__icon md-icon"></span>
      On this page
    </label>
    <ul class="md-nav__list" data-md-component="toc" data-md-scrollfix>
      
        <li class="md-nav__item">
  <a href="#what-the-history-actually-contained" class="md-nav__link">
    <span class="md-ellipsis">
      <span class="md-typeset">
        What the history actually contained
      </span>
    </span>
  </a>
  
</li>
      
        <li class="md-nav__item">
  <a href="#the-same-complaint-filed-by-hundreds" class="md-nav__link">
    <span class="md-ellipsis">
      <span class="md-typeset">
        The same complaint, filed by hundreds
      </span>
    </span>
  </a>
  
</li>
      
        <li class="md-nav__item">
  <a href="#two-caches-two-answers" class="md-nav__link">
    <span class="md-ellipsis">
      <span class="md-typeset">
        Two caches, two answers
      </span>
    </span>
  </a>
  
</li>
      
        <li class="md-nav__item">
  <a href="#the-cleanup-step-by-step" class="md-nav__link">
    <span class="md-ellipsis">
      <span class="md-typeset">
        The cleanup, step by step
      </span>
    </span>
  </a>
  
</li>
      
        <li class="md-nav__item">
  <a href="#why-i-consider-the-default-unethical" class="md-nav__link">
    <span class="md-ellipsis">
      <span class="md-typeset">
        Why I consider the default unethical
      </span>
    </span>
  </a>
  
</li>
      
        <li class="md-nav__item">
  <a href="#what-keeps-it-from-happening-again" class="md-nav__link">
    <span class="md-ellipsis">
      <span class="md-typeset">
        What keeps it from happening again
      </span>
    </span>
  </a>
  
</li>
      
        <li class="md-nav__item">
  <a href="#what-i-took-from-it" class="md-nav__link">
    <span class="md-ellipsis">
      <span class="md-typeset">
        What I took from it
      </span>
    </span>
  </a>
  
</li>
      
        <li class="md-nav__item">
  <a href="#sources-and-discussions" class="md-nav__link">
    <span class="md-ellipsis">
      <span class="md-typeset">
        Sources and discussions
      </span>
    </span>
  </a>
  
</li>
      
    </ul>
  
</nav>
      
    </li>
  

                
              
            </ul>
          </nav>
        
      
    </li>
  

                
              
                
                  
  
  
  
  
    
    
    
    
      
    
    
      
        
        
      
    
    <li class="md-nav__item md-nav__item--pruned md-nav__item--nested">
      
        
  
  
  
  
    <a href="../../Hermes/browseros-hermes-guide/" class="md-nav__link">
      
  
  
  <span class="md-ellipsis">
    
  
  Hermes

    
  </span>
  
  

      
        <span class="md-nav__icon md-icon"></span>
      
    </a>
  

      
    </li>
  

                
              
                
                  
  
  
  
  
    
    
    
    
      
    
    
      
        
        
      
    
    <li class="md-nav__item md-nav__item--pruned md-nav__item--nested">
      
        
  
  
  
  
    <a href="../../LLMs/dolphin-llm-guide/" class="md-nav__link">
      
  
  
  <span class="md-ellipsis">
    
  
  LLMs

    
  </span>
  
  

      
        <span class="md-nav__icon md-icon"></span>
      
    </a>
  

      
    </li>
  

                
              
                
                  
  
  
  
  
    
    
    
    
      
    
    
      
        
        
      
    
    <li class="md-nav__item md-nav__item--pruned md-nav__item--nested">
      
        
  
  
  
  
    <a href="../../OpenCode/notebooklm-opencode-tutorial/" class="md-nav__link">
      
  
  
  <span class="md-ellipsis">
    
  
  OpenCode

    
  </span>
  
  

      
        <span class="md-nav__icon md-icon"></span>
      
    </a>
  

      
    </li>
  

                
              
            </ul>
          </nav>
        
      
    </li>
  

    
      
      
  
  
  
  
    
    
    
    
      
        
        
      
    
    
      
    
    <li class="md-nav__item md-nav__item--section md-nav__item--nested">
      
        
        
        <input class="md-nav__toggle md-toggle " type="checkbox" id="__nav_5" >
        
          
          <label class="md-nav__link" for="__nav_5" id="__nav_5_label" tabindex="">
            
  
  
  <span class="md-ellipsis">
    
  
  JS TS

    
  </span>
  
  

            <span class="md-nav__icon md-icon"></span>
          </label>
        
        
          <nav class="md-nav" data-md-level="1" aria-labelledby="__nav_5_label" aria-expanded="false">
            <label class="md-nav__title" for="__nav_5">
              <span class="md-nav__icon md-icon"></span>
              
  
  JS TS

            </label>
            <ul class="md-nav__list" data-md-scrollfix>
              
                
                  
  
  
  
  
    <li class="md-nav__item">
      <a href="../../../JS-TS/" class="md-nav__link">
        
  
  
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><title>TypeScript</title><path d="M1.125 0C.502 0 0 .502 0 1.125v21.75C0 23.498.502 24 1.125 24h21.75c.623 0 1.125-.502 1.125-1.125V1.125C24 .502 23.498 0 22.875 0zm17.363 9.75q.918 0 1.627.111a6.4 6.4 0 0 1 1.306.34v2.458a4 4 0 0 0-.643-.361 5 5 0 0 0-.717-.26 5.5 5.5 0 0 0-1.426-.2q-.45 0-.819.086a2.1 2.1 0 0 0-.623.242q-.254.156-.393.374a.9.9 0 0 0-.14.49q0 .294.156.529.156.234.443.444c.287.21.423.276.696.41q.41.203.926.416.705.296 1.266.628.561.333.963.753.402.418.614.957.213.538.214 1.253 0 .986-.373 1.656a3.03 3.03 0 0 1-1.012 1.085 4.4 4.4 0 0 1-1.487.596q-.85.18-1.79.18a10 10 0 0 1-1.84-.164 5.5 5.5 0 0 1-1.512-.493v-2.63a5.03 5.03 0 0 0 3.237 1.2q.5 0 .872-.09.373-.09.623-.25.249-.162.373-.38a1.02 1.02 0 0 0-.074-1.089 2.1 2.1 0 0 0-.537-.5 5.6 5.6 0 0 0-.807-.444 28 28 0 0 0-1.007-.436q-1.377-.575-2.053-1.405t-.676-2.005q0-.92.369-1.582.368-.662 1.004-1.089a4.5 4.5 0 0 1 1.47-.629 7.5 7.5 0 0 1 1.77-.201m-15.113.188h9.563v2.166H9.506v9.646H6.789v-9.646H3.375z"/></svg>
  
  <span class="md-ellipsis">
    
  
  JS and TS

    
  </span>
  
  

      </a>
    </li>
  

                
              
                
                  
  
  
  
  
    <li class="md-nav__item">
      <a href="../../../JS-TS/oxc-formatting/" class="md-nav__link">
        
  
  
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><title>TypeScript</title><path d="M1.125 0C.502 0 0 .502 0 1.125v21.75C0 23.498.502 24 1.125 24h21.75c.623 0 1.125-.502 1.125-1.125V1.125C24 .502 23.498 0 22.875 0zm17.363 9.75q.918 0 1.627.111a6.4 6.4 0 0 1 1.306.34v2.458a4 4 0 0 0-.643-.361 5 5 0 0 0-.717-.26 5.5 5.5 0 0 0-1.426-.2q-.45 0-.819.086a2.1 2.1 0 0 0-.623.242q-.254.156-.393.374a.9.9 0 0 0-.14.49q0 .294.156.529.156.234.443.444c.287.21.423.276.696.41q.41.203.926.416.705.296 1.266.628.561.333.963.753.402.418.614.957.213.538.214 1.253 0 .986-.373 1.656a3.03 3.03 0 0 1-1.012 1.085 4.4 4.4 0 0 1-1.487.596q-.85.18-1.79.18a10 10 0 0 1-1.84-.164 5.5 5.5 0 0 1-1.512-.493v-2.63a5.03 5.03 0 0 0 3.237 1.2q.5 0 .872-.09.373-.09.623-.25.249-.162.373-.38a1.02 1.02 0 0 0-.074-1.089 2.1 2.1 0 0 0-.537-.5 5.6 5.6 0 0 0-.807-.444 28 28 0 0 0-1.007-.436q-1.377-.575-2.053-1.405t-.676-2.005q0-.92.369-1.582.368-.662 1.004-1.089a4.5 4.5 0 0 1 1.47-.629 7.5 7.5 0 0 1 1.77-.201m-15.113.188h9.563v2.166H9.506v9.646H6.789v-9.646H3.375z"/></svg>
  
  <span class="md-ellipsis">
    
  
  OXC Formatter Guide

    
  </span>
  
  

      </a>
    </li>
  

                
              
            </ul>
          </nav>
        
      
    </li>
  

    
      
      
  
  
  
  
    
    
    
    
      
        
        
      
    
    
      
    
    <li class="md-nav__item md-nav__item--section md-nav__item--nested">
      
        
        
        <input class="md-nav__toggle md-toggle " type="checkbox" id="__nav_6" >
        
          
          <label class="md-nav__link" for="__nav_6" id="__nav_6_label" tabindex="">
            
  
  
  <span class="md-ellipsis">
    
  
  Linux

    
  </span>
  
  

            <span class="md-nav__icon md-icon"></span>
          </label>
        
        
          <nav class="md-nav" data-md-level="1" aria-labelledby="__nav_6_label" aria-expanded="false">
            <label class="md-nav__title" for="__nav_6">
              <span class="md-nav__icon md-icon"></span>
              
  
  Linux

            </label>
            <ul class="md-nav__list" data-md-scrollfix>
              
                
                  
  
  
  
  
    <li class="md-nav__item">
      <a href="../../../Linux/" class="md-nav__link">
        
  
  
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="lucide lucide-terminal" viewBox="0 0 24 24"><path d="M12 19h8M4 17l6-6-6-6"/></svg>
  
  <span class="md-ellipsis">
    
  
  Linux

    
  </span>
  
  

      </a>
    </li>
  

                
              
                
                  
  
  
  
  
    <li class="md-nav__item">
      <a href="../../../Linux/samba-folder-share-guide/" class="md-nav__link">
        
  
  
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="lucide lucide-server" viewBox="0 0 24 24"><rect width="20" height="8" x="2" y="2" rx="2" ry="2"/><rect width="20" height="8" x="2" y="14" rx="2" ry="2"/><path d="M6 6h.01M6 18h.01"/></svg>
  
  <span class="md-ellipsis">
    
  
  A Careful Samba Folder Share on Debian-Based Linux

    
  </span>
  
  

      </a>
    </li>
  

                
              
            </ul>
          </nav>
        
      
    </li>
  

    
  </ul>
</nav>
                  </div>
                </div>
              </div>
            
            
              
              <div class="md-sidebar md-sidebar--secondary" data-md-component="sidebar" data-md-type="toc" >
                <div class="md-sidebar__scrollwrap">
                  
                    
                    
                    
                    
                      <input class="md-nav__toggle md-toggle" type="checkbox" id="__toc">
                      <div class="md-sidebar-button__wrapper">
                        <label class="md-sidebar-button" for="__toc"></label>
                      </div>
                    
                  
                  <div class="md-sidebar__inner">
                    


<nav class="md-nav md-nav--secondary" aria-label="On this page">
  
  
  
  
    <label class="md-nav__title" for="__toc">
      <span class="md-nav__icon md-icon"></span>
      On this page
    </label>
    <ul class="md-nav__list" data-md-component="toc" data-md-scrollfix>
      
        <li class="md-nav__item">
  <a href="#what-the-history-actually-contained" class="md-nav__link">
    <span class="md-ellipsis">
      <span class="md-typeset">
        What the history actually contained
      </span>
    </span>
  </a>
  
</li>
      
        <li class="md-nav__item">
  <a href="#the-same-complaint-filed-by-hundreds" class="md-nav__link">
    <span class="md-ellipsis">
      <span class="md-typeset">
        The same complaint, filed by hundreds
      </span>
    </span>
  </a>
  
</li>
      
        <li class="md-nav__item">
  <a href="#two-caches-two-answers" class="md-nav__link">
    <span class="md-ellipsis">
      <span class="md-typeset">
        Two caches, two answers
      </span>
    </span>
  </a>
  
</li>
      
        <li class="md-nav__item">
  <a href="#the-cleanup-step-by-step" class="md-nav__link">
    <span class="md-ellipsis">
      <span class="md-typeset">
        The cleanup, step by step
      </span>
    </span>
  </a>
  
</li>
      
        <li class="md-nav__item">
  <a href="#why-i-consider-the-default-unethical" class="md-nav__link">
    <span class="md-ellipsis">
      <span class="md-typeset">
        Why I consider the default unethical
      </span>
    </span>
  </a>
  
</li>
      
        <li class="md-nav__item">
  <a href="#what-keeps-it-from-happening-again" class="md-nav__link">
    <span class="md-ellipsis">
      <span class="md-typeset">
        What keeps it from happening again
      </span>
    </span>
  </a>
  
</li>
      
        <li class="md-nav__item">
  <a href="#what-i-took-from-it" class="md-nav__link">
    <span class="md-ellipsis">
      <span class="md-typeset">
        What I took from it
      </span>
    </span>
  </a>
  
</li>
      
        <li class="md-nav__item">
  <a href="#sources-and-discussions" class="md-nav__link">
    <span class="md-ellipsis">
      <span class="md-typeset">
        Sources and discussions
      </span>
    </span>
  </a>
  
</li>
      
    </ul>
  
</nav>
                  </div>
                </div>
              </div>
            
          
          
            <div class="md-content" data-md-component="content">
              
                



  


  <nav class="md-path" aria-label="Navigation" >
    <ol class="md-path__list">
      
        
  
  
    <li class="md-path__item">
      <a href="../../.." class="md-path__link">
        
  
  <span class="md-ellipsis">
    Code Sigils
  </span>

      </a>
    </li>
  

      
      
        
  
  
    
    
    
    
    
      <li class="md-path__item">
        <a href="../../" class="md-path__link">
          
  
  <span class="md-ellipsis">
    AI
  </span>

        </a>
      </li>
    
  

      
        
  
  
    
    
    
    
    
      <li class="md-path__item">
        <a href="../agent-instruction-drift/" class="md-path__link">
          
  
  <span class="md-ellipsis">
    Agent Work
  </span>

        </a>
      </li>
    
  

      
    </ol>
  </nav>

              
              <article class="md-content__inner md-typeset">
                
                  

  <h1 id="__skip">When an AI Agent Signs Your Commits</h1>

<p>The contributors widget on a GitHub repository looks like a plain statement of
fact: avatars, names, a count. When this blog's repository started listing an
AI agent next to my own account, the first question was whether the widget was
simply wrong. It was not wrong, exactly. Two commits in the history carried
attribution I had never agreed to: a <code>Co-authored-by</code> trailer naming an AI
agent, and a branding line at the bottom of a commit message reading
<code>Ultraworked with [Sisyphus](https://github.com/...)</code>.</p>
<p>The question I kept coming back to was simple: who authorised this, and what is
the remedy when nobody agrees it should be there?</p>
<h2 id="what-the-history-actually-contained">What the history actually contained<a class="headerlink" href="#what-the-history-actually-contained" title="Permanent link">&para;</a></h2>
<p>The trailers were small. One documentation commit ended with
<code>Co-authored-by: Sisyphus &lt;clio-agent@sisyphuslabs.ai&gt;</code>; another ended with the
branding line above. Both were added by agent tooling during an ordinary
work session, the way these frameworks credit the tool that produced the
change. GitHub parses commit messages at render time, so a trailer written
months ago can change a widget today (<a href="https://docs.github.com/en/pull-requests/committing-changes-to-your-project/creating-commits-with-co-authored-attributions">GitHub's co-author
documentation</a>
explains the format and how GitHub turns trailers into credits).</p>
<p>What made this easy to miss is that <code>git log</code>'s default view shows subjects,
instead of the expected bodies. The trailers sat several lines down in messages I had no reason to
reopen. The same experience shows up well beyond this repository: a
<a href="https://github.com/anthropics/claude-code/issues/83813">claude-code
discussion</a> describes
an attribution trailer sitting 123 commits deep before anyone noticed, with
tags, open pull requests, and uncollected garbage keeping the old objects
reachable long after the author had decided to remove it.</p>
<h2 id="the-same-complaint-filed-by-hundreds">The same complaint, filed by hundreds<a class="headerlink" href="#the-same-complaint-filed-by-hundreds" title="Permanent link">&para;</a></h2>
<p>My trailer came from an agent framework rather than an IDE plugin, but the
pattern was reported by users across multiple tools. Claude Code is the most documented case: its
commit workflow appends <code>Co-Authored-By: Claude &lt;noreply@anthropic.com&gt;</code> by
default, and a long trail of issues in the
<a href="https://github.com/anthropics/claude-code/issues">claude-code</a> tracker asks
for that default to change.</p>
<ul>
<li><a href="https://github.com/anthropics/claude-code/issues/48145">Issue #48145</a>,
  titled "should be opt-in", reports a user finding the trailer on every
  public commit they had pushed and arguing that documentation buried in a
  system prompt is not consent.</li>
<li><a href="https://github.com/anthropics/claude-code/issues/7422">Issue #7422</a>
  records the trailer being added even when the project's <code>CLAUDE.md</code> says,
  in those words, "DO NOT put this in the commit message".</li>
<li><a href="https://github.com/anthropics/claude-code/issues/53259">Issue #53259</a>
  catalogues the failed escape hatches: <code>settings.json</code>, <code>CLAUDE.md</code>, custom
  skills, and explicit in-session instructions, with different commit code
  paths in the same session disagreeing about whether to honour them. A
  maintainer in <a href="https://github.com/anthropics/claude-code/issues/79909">issue #79909</a>
  states that an empty <code>attribution.commit</code> setting is the supported switch
  and verifies it, while other reporters say the same key did nothing for
  them; even that disagreement is part of the problem.</li>
<li><a href="https://github.com/anthropics/claude-code/issues/64019">Issue #64019</a>
  describes the same repair I ended up running here: a full <code>filter-branch</code>
  pass and force push across the whole history. The reporter in #79909 got
  there too, after a trailer reached a private organisation repository and
  needed <code>git commit --amend</code> plus <code>--force-with-lease</code>.</li>
</ul>
<p>The complaint, in my opinion, is ethical as much as technical. One recurring theme across
those threads is that the trailer presents the tool as a co-author of the
user's work, in the user's name, without anything the user would recognise
as an approval step.</p>
<p>Codex, by contrast, has so far followed the cleaner practice. Its CLI does
not append a co-author trailer by default: a January 2026 analysis on
OpenAI's community forum, examining a dataset of AI-assisted commits, found
no commit-level attribution or metadata in Codex-associated commits at all
(<a href="https://community.openai.com/t/does-openai-codex-add-any-default-commit-level-metadata-in-git-workflows/1371947">community analysis</a>).
When the option exists, it sits behind an opt-in feature flag
(<code>codex_git_commit</code>, with <code>commit_attribution = ""</code> disabling even that),
merged in early 2026 rather than assumed at install time
(<a href="https://github.com/openai/codex/issues/19799">issue #19799</a> tracks the
remaining documentation ambiguity). The request threads run in the opposite
direction from Claude's: <a href="https://github.com/openai/codex/discussions/2807">discussion #2807</a>
and <a href="https://github.com/openai/codex/issues/938">issue #938</a> ask Codex to
<em>add</em> a trailer for teams that want disclosure, as parity with Claude Code.
Nobody in those threads is trying to get attribution out of their history.</p>
<p>It's a telling sign of how common this has become: people have built
tools specifically to remove these co-author trailers. For example, the
<a href="https://github.com/Londopy/git-attribution">git-attribution</a> tool
can scan commit history, strip known agent trailers, and even prevent them
from being added again. When you need special tools just to undo something
that shouldn't have been added in the first place, that says a lot about
the default.</p>
<h2 id="two-caches-two-answers">Two caches, two answers<a class="headerlink" href="#two-caches-two-answers" title="Permanent link">&para;</a></h2>
<p>The first cleanup pass rewrote the three affected commit messages, and the
file contents stayed byte-identical (verified with <code>git diff</code> against a backup
ref before the backup was removed). Then the surfaces started disagreeing:</p>
<ul>
<li>The REST <code>/contributors</code> endpoint returned exactly one account, mine.</li>
<li>The homepage sidebar widget still credited the AI agent.</li>
<li>The Insights contributors graph had already forgotten it after the
  force-push.</li>
</ul>
<p>The best measurements I found come
from <a href="https://github.com/ParkerrDev/declaudify">declaudify</a>, a tool built
precisely to flush this kind of stale attribution. Its author tested the
behaviour rather than assuming it: GitHub renders contributors from two
separate caches, a force-push clears the Insights graph but not the homepage
sidebar, extra commits do not help, and archive/unarchive does nothing.
Toggling the default branch is what clears the sidebar, in his measurements
between 60 and 81 seconds across three trials. The REST <code>/contributors</code>
endpoint omits co-authors entirely, which is why an API check can look clean
while the widget still names an AI account.</p>
<p>Community reports match the shape of that problem:</p>
<ul>
<li><a href="https://github.com/orgs/community/discussions/205858">Discussion #205858</a>
  includes a staff reply: "I've refreshed the contributors list, so it should
  be up to date now." Several other affected repositories are listed by their
  owners in the same thread.</li>
<li><a href="https://github.com/orgs/community/discussions/201982">Discussion #201982</a>
  reports a stale contributor list lasting more than a month, with a checklist
  of nudges: empty commit, edit the repository description, check tags and
  branches for the old SHA, verify in a logged-out window.</li>
<li><a href="https://github.com/orgs/community/discussions/205779">Discussions #205779</a>,
  <a href="https://github.com/orgs/community/discussions/204093">#204093</a>, and
  <a href="https://github.com/orgs/community/discussions/202538">#202538</a> show the
  same pattern: REST and Insights clean, sidebar still crediting an AI account.</li>
<li><a href="https://github.com/orgs/community/discussions/202540">Discussions #202540</a>
  and <a href="https://github.com/orgs/community/discussions/198886">#198886</a> report
  sidebar staleness measured in weeks.</li>
</ul>
<table>
<thead>
<tr>
<th style="text-align: left;">Surface</th>
<th style="text-align: left;">What it reads</th>
<th style="text-align: left;">How it actually refreshed</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;">Insights graph</td>
<td style="text-align: left;">the rewritten history</td>
<td style="text-align: left;">force-push (per declaudify's tests)</td>
</tr>
<tr>
<td style="text-align: left;">REST <code>/contributors</code></td>
<td style="text-align: left;">commit authorship, no co-authors</td>
<td style="text-align: left;">updated with the rewrite</td>
</tr>
<tr>
<td style="text-align: left;">Homepage sidebar widget</td>
<td style="text-align: left;">its own cache of parsed trailers</td>
<td style="text-align: left;">default-branch toggle, staff refresh, or the documented wait</td>
</tr>
</tbody>
</table>
<p>I also found a cheap way to check the widget's real data source without a
browser: GitHub's JSON payload for the repository route. A <code>GET</code> on the
repository page with <code>Accept: application/json</code> returns the rendered route,
and the same header on the <code>/_sidebar</code> path returns the widget's feed
directly:</p>
<div class="language-bash highlight"><pre><span></span><code><span id="__span-0-1">curl<span class="w"> </span>-s<span class="w"> </span>-H<span class="w"> </span><span class="s2">"Accept: application/json"</span><span class="w"> </span><span class="se">\</span>
</span><span id="__span-0-2"><span class="w">  </span>https://github.com/CodeSigils/CodeSigils.github.io/_sidebar
</span></code></pre></div>
<p>After the flush, that feed reported <code>contributorCount: 1</code>. Checking the data
source rather than the rendered page settled the question in one request.</p>
<h2 id="the-cleanup-step-by-step">The cleanup, step by step<a class="headerlink" href="#the-cleanup-step-by-step" title="Permanent link">&para;</a></h2>
<p>Nothing about the remediation is complicated individually. The difficulty is
that no single document lists the sequence.</p>
<p><strong>1. Rewrite the messages, not the tree.</strong> A <code>git filter-branch</code> pass with a
message filter over the affected range strips the offending lines while
leaving every file byte-identical:</p>
<div class="language-bash highlight"><pre><span></span><code><span id="__span-1-1">git<span class="w"> </span>filter-branch<span class="w"> </span>-f<span class="w"> </span>--msg-filter<span class="w"> </span><span class="se">\</span>
</span><span id="__span-1-2"><span class="w">  </span><span class="s2">"grep -v -e '^Co-authored-by: ' -e '^Ultraworked with '"</span><span class="w"> </span><span class="se">\</span>
</span><span id="__span-1-3"><span class="w">  </span>3deab8c..master
</span></code></pre></div>
<p><a href="https://github.com/newren/filter-repo">filter-repo</a> is the more modern tool
for the same job; I used <code>filter-branch</code> for a three-commit range where the
surgical fix was smaller than the migration.</p>
<p><strong>2. Push the rewrite and purge the remnants.</strong> <code>git push --force-with-lease</code>
updates the remote, then the local backup refs, <code>ORIG_HEAD</code>, and reflogs have
to go (<code>git reflog expire --expire=now --all &amp;&amp; git gc --prune=now</code>), or the
old SHAs stay alive locally and the cleanup looks incomplete to the next
<code>git fsck</code>.</p>
<p><strong>3. Re-queue GitHub's metadata refresh.</strong> An empty commit with a mundane
message (<code>chore: refresh repository metadata</code>) gives GitHub's jobs something
new to index. This alone does not clear the sidebar.</p>
<p><strong>4. The drastic part: toggle the default branch.</strong> This is the sequence that
actually flushed the widget cache:</p>
<div class="language-bash highlight"><pre><span></span><code><span id="__span-2-1">gh<span class="w"> </span>auth<span class="w"> </span>status
</span><span id="__span-2-2">git<span class="w"> </span>push<span class="w"> </span>origin<span class="w"> </span>master:refresh/sidebar-flush
</span><span id="__span-2-3">gh<span class="w"> </span>api<span class="w"> </span>-X<span class="w"> </span>PATCH<span class="w"> </span>/repos/CodeSigils/CodeSigils.github.io<span class="w"> </span>-f<span class="w"> </span><span class="nv">default_branch</span><span class="o">=</span>refresh/sidebar-flush
</span><span id="__span-2-4">sleep<span class="w"> </span><span class="m">90</span>
</span><span id="__span-2-5">gh<span class="w"> </span>api<span class="w"> </span>-X<span class="w"> </span>PATCH<span class="w"> </span>/repos/CodeSigils/CodeSigils.github.io<span class="w"> </span>-f<span class="w"> </span><span class="nv">default_branch</span><span class="o">=</span>master
</span><span id="__span-2-6">git<span class="w"> </span>push<span class="w"> </span>origin<span class="w"> </span>--delete<span class="w"> </span>refresh/sidebar-flush
</span></code></pre></div>
<p>What each line does: <code>gh auth status</code> confirms the token carries admin rights,
because changing the default branch is an administrative operation. The second
line pushes <code>master</code> to a temporary branch name without touching local state.
The first <code>PATCH</code> makes that branch the repository's default, which forces
GitHub to recompute the repository's route data, sidebar included. <code>sleep 90</code>
covers the 60-to-81-second window declaudify measured, with margin. The second
<code>PATCH</code> restores <code>master</code> as the default, and the last line deletes the
temporary branch. No content changes at any point; the repository ends exactly
where it started, minus the stale cache.</p>
<div class="admonition warning">
<p class="admonition-title">Flush only after the index is clean</p>
<p>The author of <a href="https://github.com/ediiloupatty/declaude">declaude</a> warns
that flushing caches while GitHub still serves the old commit index can
rebuild the graph from the old history and re-insert the AI credit. Verify
through the API and commit search that the remote history is clean first,
then flush, then verify again, retrying up to three times if the widget
comes back wrong.</p>
</div>
<p>One residual worth knowing: rewritten commits remain reachable by their old
SHA and through <code>refs/pull/N/head</code> if pull requests existed. Neither surface
feeds the contributor widgets, but in the claude-code discussion above, one
reporter's old commits stayed alive through three open pull requests and
required GitHub Support to delete them, over two rounds of tickets. This
repository had no pull requests holding the old objects, so the purge was
clean.</p>
<h2 id="why-i-consider-the-default-unethical">Why I consider the default unethical<a class="headerlink" href="#why-i-consider-the-default-unethical" title="Permanent link">&para;</a></h2>
<p>I consider non-consensual AI attribution in commit messages an unethical
practice, and the cleanup is what convinced me.</p>
<p>A commit trailer is an assertion of authorship. When tooling writes that
assertion in my commits by default, it forges a provenance claim I never
approved: it presents an AI agent as a co-author of my writing, under my name,
in a public record. Consent is absent at every step. The addition is
automatic, the display is asynchronous, and the person credited with the
mistake is the one who has to undo it.</p>
<p>What makes it worse is the response on the other side. I found no official
guidance addressing unwanted attribution from agent tooling. GitHub's
documentation explains how to add co-authors and how to remove one from a
commit before it is shared; once the commit is pushed and the caches have
eaten it, the published remedy for stale contributor data amounts to "wait up
to 24 hours, then contact Support," as quoted by staff in
<a href="https://github.com/orgs/community/discussions/205858">discussion #205858</a>.
There is no button, no API, no documented procedure for the person whose
repository is misrepresenting authorship. The working knowledge lives in
community threads where affected owners compare notes and occasionally
persuade a staff member to refresh a list by hand.</p>
<p>So the burden sits entirely with the author: discover the problem, learn that
the widget and the API disagree, find a tool author's measurement of which
cache clears how, rewrite history, and toggle a branch switch as a cache
flush. That asymmetry is the ethical failure in one sentence: a practice that
creates a false authorship claim, with no concern from the tooling that adds
it and no clear remedy on the platform that displays it.</p>
<h2 id="what-keeps-it-from-happening-again">What keeps it from happening again<a class="headerlink" href="#what-keeps-it-from-happening-again" title="Permanent link">&para;</a></h2>
<p>The lesson I took is that attribution has to be enforced by machinery at more
than one layer, because instructions alone demonstrably lose. The
claude-code discussion is the clearest evidence: one reporter's
<code>attribution</code> settings were configured to suppress commits and pull-request
credits, and the trailer appeared anyway; the conclusion reached in that
thread was that only a command-level hook inspecting tool calls before they
run, plus a CI gate failing on attribution patterns, can be trusted.</p>
<p>What exists in this repository now:</p>
<ul>
<li><strong>A written policy.</strong> This repository's <code>AGENTS.md</code> carries a Git Commit
  Policy section: no <code>Co-authored-by:</code> trailers of any kind, no bot accounts,
  no agent branding lines, no <code>--no-verify</code>. My local agent instructions
  carry the same rule.</li>
<li><strong>A local <code>commit-msg</code> hook</strong> rejecting forbidden trailers and branding
  lines, built on <a href="https://pre-commit.com/">pre-commit</a> with a pygrep rule.
  It fires on <code>commit</code>, <code>commit --amend</code>, and interactive reword. It does not
  fire on cherry-picks, and <code>--no-verify</code> walks past it — which is why it is
  the first layer, not the only one. The other candidates I evaluated:
  <a href="https://jorisroovers.com/gitlint/">gitlint</a> has been dormant since its
  2023 release and offers no must-not-match rule at all, and
  <a href="https://commitlint.js.org/">commitlint</a> would need a custom plugin for a
  deny rule.</li>
<li><strong>A CI backstop</strong> that scans pushed commit messages and fails the build on
  the same patterns. A hook can be skipped with <code>--no-verify</code>, which my
  policy treats as a violation in itself; a CI check cannot be skipped from
  a laptop. It cannot refuse the push itself — on a push event it can only
  flag what has already landed — but a red run on <code>master</code> is a signal that
  triggers the rewrite procedure above.</li>
</ul>
<h2 id="what-i-took-from-it">What I took from it<a class="headerlink" href="#what-i-took-from-it" title="Permanent link">&para;</a></h2>
<p>Rendered summaries are caches with opinions. The widget was neither lying nor
telling the whole truth; it was serving a different index than the API I
checked first, and trusting the first clean answer would have ended the
investigation one layer too early. Since then I read the data source before I
believe the page, and I treat every claim my history makes about authorship
as something I am responsible for. An agent can write the commit. It does not
get to sign it.</p>
<h2 id="sources-and-discussions">Sources and discussions<a class="headerlink" href="#sources-and-discussions" title="Permanent link">&para;</a></h2>
<p><strong>Incidents and community reports</strong></p>
<ul>
<li><a href="https://github.com/orgs/community/discussions/205858">Community discussion #205858</a>
  — staff refresh reply, 24-hour guidance quoted, multiple affected repositories.</li>
<li><a href="https://github.com/orgs/community/discussions/201982">Community discussion #201982</a>
  — stale beyond a month, nudge checklist.</li>
<li><a href="https://github.com/orgs/community/discussions/205779">Discussions #205779</a>,
  <a href="https://github.com/orgs/community/discussions/204093">#204093</a>,
  <a href="https://github.com/orgs/community/discussions/202538">#202538</a>,
  <a href="https://github.com/orgs/community/discussions/202540">#202540</a>,
  <a href="https://github.com/orgs/community/discussions/198886">#198886</a> — sidebar
  staleness and API/widget disagreement.</li>
<li><a href="https://github.com/anthropics/claude-code/issues/83813">anthropics/claude-code issue #83813</a>
  — instruction-level attribution settings losing, deep-trailer incident,
  PR-held objects, machine-enforcement conclusion.</li>
</ul>
<p><strong>Other agents' defaults</strong></p>
<ul>
<li><a href="https://github.com/anthropics/claude-code/issues/48145">claude-code #48145</a>
  — "this should be opt-in", consent argument.</li>
<li><a href="https://github.com/anthropics/claude-code/issues/7422">claude-code #7422</a>
  — trailer added against explicit <code>CLAUDE.md</code> instructions.</li>
<li><a href="https://github.com/anthropics/claude-code/issues/53259">claude-code #53259</a>
  — catalogue of failed overrides and code-path inconsistency.</li>
<li><a href="https://github.com/anthropics/claude-code/issues/79909">claude-code #79909</a>
  — recurrence after in-conversation instruction; maintainer's supported
  <code>attribution.commit</code> switch.</li>
<li><a href="https://github.com/anthropics/claude-code/issues/64019">claude-code #64019</a>
  — full-history <code>filter-branch</code> cleanup account.</li>
<li><a href="https://community.openai.com/t/does-openai-codex-add-any-default-commit-level-metadata-in-git-workflows/1371947">OpenAI community analysis of AI-assisted commits</a>
  — no commit-level metadata found in Codex commits (January 2026).</li>
<li><a href="https://github.com/openai/codex/issues/19799">openai/codex #19799</a> —
  attribution behaviour documentation gap.</li>
<li><a href="https://github.com/openai/codex/discussions/2807">openai/codex discussion #2807</a>
  and <a href="https://github.com/openai/codex/issues/938">#938</a> — requests to add
  a trailer, not remove one.</li>
<li><a href="https://github.com/Londopy/git-attribution">Londopy/git-attribution</a> —
  multi-agent trailer scanner, rewriter, and pre-push guard.</li>
</ul>
<p><strong>Tools and measurements</strong></p>
<ul>
<li><a href="https://github.com/ParkerrDev/declaudify">ParkerrDev/declaudify</a> —
  two-cache model, default-branch toggle timings, REST endpoint behaviour.</li>
<li><a href="https://github.com/ediiloupatty/declaude">ediiloupatty/declaude</a> — flush
  ordering caution and retry guidance.</li>
<li><a href="https://github.com/newren/filter-repo">newren/filter-repo</a> — history
  rewriting.</li>
</ul>
<p><strong>Official documentation</strong></p>
<ul>
<li><a href="https://docs.github.com/en/pull-requests/committing-changes-to-your-project/creating-commits-with-co-authored-attributions">Creating commits with co-authored
  attributions</a>
  — GitHub's format and rendering rules.</li>
<li><a href="https://pre-commit.com/">pre-commit</a>, <a href="https://jorisroovers.com/gitlint/">gitlint</a>,
  <a href="https://commitlint.js.org/">commitlint</a> — candidate enforcement frameworks.</li>
</ul>
<p><strong>On this site</strong></p>
<ul>
<li><a href=".././agent-instruction-drift/">When Agent Instructions Start to Drift</a> —
  the maintenance problem that duplicated rules create.</li>
<li><a href=".././agent-memory-surfaces/">Agent Memory Is a Surface, Not an Archive</a> —
  what agent-side persistence actually keeps.</li>
</ul>
<p>Links were reachable when this article was written in October 2026.</p>









  
  






                
              </article>
            </div>
          
          
  <script>var tabs=__md_get("__tabs");if(Array.isArray(tabs))e:for(var set of document.querySelectorAll(".tabbed-set")){var labels=set.querySelector(".tabbed-labels");for(var tab of tabs)for(var label of labels.getElementsByTagName("label"))if(label.innerText.trim()===tab){var input=document.getElementById(label.htmlFor);input.checked=!0;continue e}}</script>

<script>var target=document.getElementById(location.hash.slice(1));target&&target.name&&(target.checked=target.name.startsWith("__tabbed_"))</script>
        </div>
        
          <button type="button" class="md-top md-icon" data-md-component="top" hidden>
  
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="lucide lucide-circle-arrow-up" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="m16 12-4-4-4 4M12 16V8"/></svg>
  Back to top
</button>
        
      </main>
      
        <footer class="md-footer">
  
    
      
      <nav class="md-footer__inner md-grid" aria-label="Footer" >
        
          
          <a href="../agent-memory-surfaces/" class="md-footer__link md-footer__link--prev" aria-label="Previous: Where an Agent&#x27;s Memory Actually Lives">
            <div class="md-footer__button md-icon">
              
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="lucide lucide-arrow-left" viewBox="0 0 24 24"><path d="m12 19-7-7 7-7M19 12H5"/></svg>
            </div>
            <div class="md-footer__title">
              <span class="md-footer__direction">
                Previous
              </span>
              <div class="md-ellipsis">
                Where an Agent's Memory Actually Lives
              </div>
            </div>
          </a>
        
        
          
          <a href="../../Hermes/browseros-hermes-guide/" class="md-footer__link md-footer__link--next" aria-label="Next: BrowserOS + Hermes Agent Integration Guide">
            <div class="md-footer__title">
              <span class="md-footer__direction">
                Next
              </span>
              <div class="md-ellipsis">
                BrowserOS + Hermes Agent Integration Guide
              </div>
            </div>
            <div class="md-footer__button md-icon">
              
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="lucide lucide-arrow-right" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </div>
          </a>
        
      </nav>
    
  
  <div class="md-footer-meta md-typeset">
    <div class="md-footer-meta__inner md-grid">
      <div class="md-copyright">
  
    <div class="md-copyright__highlight">
      Copyright &copy; 2026 Tom Geo. All rights reserved.
    </div>
  
  
    Made with
    <a href="https://zensical.org/" target="_blank" rel="noopener">
      Zensical
    </a>
  
</div>
      
        
<div class="md-social">
  
    
    
    
    
      
      
    
    <a href="https://codesigils.github.io/feed.xml" target="_blank" rel="noopener" title="codesigils.github.io" class="md-social__link">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--! Font Awesome Free 7.3.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License) Copyright 2026 Fonticons, Inc.--><path fill="currentColor" d="M0 64c0-17.7 14.3-32 32-32 229.8 0 416 186.2 416 416 0 17.7-14.3 32-32 32s-32-14.3-32-32C384 253.6 226.4 96 32 96 14.3 96 0 81.7 0 64m0 352a64 64 0 1 1 128 0 64 64 0 1 1-128 0m32-256c159.1 0 288 128.9 288 288 0 17.7-14.3 32-32 32s-32-14.3-32-32c0-123.7-100.3-224-224-224-17.7 0-32-14.3-32-32s14.3-32 32-32"/></svg>
    </a>
  
    
    
    
    
      
      
    
    <a href="https://github.com/CodeSigils" target="_blank" rel="noopener" title="github.com" class="md-social__link">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--! Font Awesome Free 7.3.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License) Copyright 2026 Fonticons, Inc.--><path fill="currentColor" d="M216.5 362.5c-66-8-112.5-55.5-112.5-117 0-25 9-52 24-70-6.5-16.5-5.5-51.5 2-66 20-2.5 47 8 63 22.5 19-6 39-9 63.5-9s44.5 3 62.5 8.5c15.5-14 43-24.5 63-22 7 13.5 8 48.5 1.5 65.5 16 19 24.5 44.5 24.5 70.5 0 61.5-46.5 108-113.5 116.5 17 11 28.5 35 28.5 62.5v52c0 15 12.5 23.5 27.5 17.5C441 459.5 512 369 512 257 512 115.5 397 0 255.5 0S0 115.5 0 257c0 111 70.5 203 165.5 237.5 13.5 5 26.5-4 26.5-17.5v-40c-7 3-16 5-24 5-33 0-52.5-18-66.5-51.5-5.5-13.5-11.5-21.5-23-23-6-.5-8-3-8-6 0-6 10-10.5 20-10.5 14.5 0 27 9 40 27.5 10 14.5 20.5 21 33 21s20.5-4.5 32-16c8.5-8.5 15-16 21-21"/></svg>
    </a>
  
    
    
    
    
      
      
    
    <a href="https://www.npmjs.com/package/zero-md-formatter" target="_blank" rel="noopener" title="www.npmjs.com" class="md-social__link">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><!--! Font Awesome Free 7.3.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License) Copyright 2026 Fonticons, Inc.--><path fill="currentColor" d="M288 288h-32v-64h32zm288-128v192H288v32H160v-32H0V160zm-416 32H32v128h64v-96h32v96h32zm160 0H192v160h64v-32h64zm224 0H352v128h64v-96h32v96h32v-96h32v96h32z"/></svg>
    </a>
  
</div>
      
    </div>
  </div>
</footer>
      
    </div>
    <div class="md-dialog" data-md-component="dialog">
      <div class="md-dialog__inner md-typeset"></div>
    </div>
    
      <div class="md-progress" data-md-component="progress" role="progressbar"></div>
    
    
    
      
      
      
      
        
        
      <script id="__config" type="application/json">{"annotate":null,"base":"../../..","features":["announce.dismiss","content.action.edit","content.action.view","content.code.annotate","content.code.copy","content.code.select","content.footnote.tooltips","content.tabs.link","content.tooltips","navigation.footer","navigation.instant","navigation.instant.prefetch","navigation.instant.progress","navigation.path","navigation.prune","navigation.sections","navigation.icons","navigation.top","navigation.tracking","search.highlight","toc.follow"],"redirect":null,"search":"../../../assets/javascripts/workers/search.7d14d953.min.js","tags":null,"translations":{"clipboard.copied":"Copied to clipboard","clipboard.copy":"Copy to clipboard","search.result.more.one":"1 more on this page","search.result.more.other":"# more on this page","search.result.none":"No matching documents","search.result.one":"1 matching document","search.result.other":"# matching documents","search.result.placeholder":"Type to start searching","search.result.term.missing":"Missing","select.version":"Select version"},"version":null}</script>
    
    
      <script src="../../../assets/javascripts/bundle.c04ba553.min.js"></script>
      
    
  </body>
</html>