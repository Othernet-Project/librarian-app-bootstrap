<!doctype html>

<html>
    <head>
        <title>App list test</title>
        <style>
        .app-list{
            padding:2em
        }

        .app-list li{
            display:inline-block;
            text-align:center;
            clear:right;
            list-style:none;
            margin-bottom:2em;
            vertical-align:top
        }

        .app-list .app-icon{
            display:inline-block;
            width:128px;
            height:128px;
            -moz-box-shadow:0 0 10px rgba(0,0,0,0.2);
            -webkit-box-shadow:0 0 10px rgba(0,0,0,0.2);
            box-shadow:0 0 10px rgba(0,0,0,0.2);
            -moz-border-radius:2px;
            -webkit-border-radius:2px;
            border-radius:2px;
            overflow:hidden
        }

        .app-list .app-version,.app-list .app-title,.app-list .app-description{
            display:block
        }

        .app-list .app-title{
            font-weight:bold
        }
        </style>
    </head>
    <body>
        <ul class="app-list">
            <li id="app-{{ app.appid }}" data-url="/en/app/" data-id="{{ app.appid }}">
                <a id="link-{{ app.appid }}" class="app-icon" href="/en/app/"><img src="/en/app/icon.png"></a>
                <div class="app-details">
                <span class="app-title"><a href="/en/app/">{{ app.title }}</a></span>
                <span class="app-description">{{ app.description[:50] }}</span>
                %# Translators, refers to app author
                <span class="app-author">{{ 'author:' }} {{ app.author }}</span>
                %# Translators, refers to app version
                <span class="app-version">{{ 'version:' }} {{ app.version }}</span>
                </div>
                % if app.icon_behavior:
                <script src="/en/app/behavior.js"></script>
                % end
            </li>
        </ul>
    </body>
</body>
    
