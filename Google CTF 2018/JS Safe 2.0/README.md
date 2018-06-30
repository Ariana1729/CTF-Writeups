# JS Safe 2.0
>You stumbled upon someone's "JS Safe" on the web. It's a simple HTML file that can store secrets in the browser's localStorage. This means that you won't be able to extract any secret from it (the secrets are on the computer of the owner), but it looks like it was hand-crafted to work only with the password of the owner...
>
>We're only given [js\_safe\_2.html](./js_safe_2.html)

Opening it, we are visited by a input box, when something is entered, we get a 'Access Denied' message. Opening the console, we see that there are 3 functions, `x(x)` and `open_safe()` and `safe()`, with the first 2 being used to verify what we typed.

```javascript
function open_safe() {
  keyhole.disabled = true;
  password = /^CTF{([0-9a-zA-Z_@!?-]+)}$/.exec(keyhole.value);
  if (!password || !x(password[1])) return document.body.className = 'denied';
  document.body.className = 'granted';
  password = Array.from(password[1]).map(c => c.charCodeAt());
  encrypted = JSON.parse(localStorage.content || '');
  content.value = encrypted.map((c,i) => c ^ password[i % password.length]).map(String.fromCharCode).join('')
}
```

Open safe compares our input to a regex, then passes our input(inside CTF{}) into the function x.

Now let's look at x():

```javascript
function x(х){ord=Function.prototype.call.bind(''.charCodeAt);chr=String.fromCharCode;str=String;function h(s){for(i=0;i!=s.length;i++){a=((typeof a=='undefined'?1:a)+ord(str(s[i])))%65521;b=((typeof b=='undefined'?0:b)+a)%65521}return chr(b>>8)+chr(b&0xFF)+chr(a>>8)+chr(a&0xFF)}function c(a,b,c){for(i=0;i!=a.length;i++)c=(c||'')+chr(ord(str(a[i]))^ord(str(b[i%b.length])));return c}for(a=0;a!=1000;a++)debugger;x=h(str(x));source=/Ӈ#7ùª9¨M¤À.áÔ¥6¦¨¹.ÿÓÂ.Ö£JºÓ¹WþÊmãÖÚG¤¢dÈ9&òªћ#³­1᧨/;source.toString=function(){return c(source,x)};try{console.log('debug',source);with(source)return eval('eval(c(source,x))')}catch(e){}}
```

Firstly let's actually make it readable:

```javascript
function x(х) {
    ord = Function.prototype.call.bind(''.charCodeAt);
    chr = String.fromCharCode;
    str = String;

    function h(s) {
        for (i = 0; i != s.length; i++) {
            a = ((typeof a == 'undefined' ? 1 : a) + ord(str(s[i]))) % 65521;
            b = ((typeof b == 'undefined' ? 0 : b) + a) % 65521
        }
        return chr(b >> 8) + chr(b & 0xFF) + chr(a >> 8) + chr(a & 0xFF)
    }

    function c(a, b, c) {
        for (i = 0; i != a.length; i++) c = (c || '') + chr(ord(str(a[i])) ^ ord(str(b[i % b.length])));
        return c
    }
    for (a = 0; a != 1000; a++) debugger;
    x = h(str(x));
    source = /Ӈ#7ùª9¨M¤À.áÔ¥6¦¨¹.ÿÓÂ.Ö£JºÓ¹WþÊmãÖÚG¤¢dÈ9&òªћ#³­1᧨/;
    source.toString = function() {
        return c(source, x)
    };
    try {
        console.log('debug', source);
        with(source) return eval('eval(c(source,x))')
    } catch (e) {}
}
```

We immediately see a anti-debugging trap, which can be removed easily by just removing `debugger;`, let's not touch the loop for now.

We see that it starts off defining `ord`, `chr`, `str`, which will function as how they do in python.

Next we have 2 nested functions, h() -> hash and c() -> cipher?.

The next part seems to be where our flag would be hiding.

# Reversing the lock
Firstly, x is passed through h, which turns it into 4 bytes

Then, source is defined as a regex with seemingly random character, and then source.tostring is overwritten, and it now returns c(source,x)

Then the functions returns with a eval of a eval of c(source,x)

It evals c()?? Seems like c() will output some code? It xors source and x, so perhaps we need to find a input that when xored with c, outputs a valid javascript?

While adding console.log(), two problems are faced:

1. The logged output keeps varying? How does adding console.log affect the function in any way or form? I got quite confused here.

2. It sometimes dies from an infinite loop when logging c(source,x)

However, when logging inputs to h, we immediately realize that the function itself is being hashed by h! That's why the results are always changing!

```
function x(х) {
    ord = Function.prototype.call.bind(''.charCodeAt);
    chr = String.fromCharCode;
    str = String;

    function h(s) {
	console.log(s)
        for (i = 0; i != s.length; i++) {
            a = ((typeof a == 'undefined' ? 1 : a) + ord(str(s[i]))) % 65521;
            b = ((typeof b == 'undefined' ? 0 : b) + a) % 65521
        }
        return chr(b >> 8) + chr(b & 0xFF) + chr(a >> 8) + chr(a & 0xFF)
    }

    function c(a, b, c) {
        console.log(a,b,c)
        for (i = 0; i != a.length; i++) c = (c || '') + chr(ord(str(a[i])) ^ ord(str(b[i % b.length])));
	console.log(c)
        return c
    }
    for (a = 0; a != 1000; a++) ;
    x = h(str(x));
    source = /Ӈ#7ùª9¨M¤À.áÔ¥6¦¨¹.ÿÓÂ.Ö£JºÓ¹WþÊmãÖÚG¤¢dÈ9&òªћ#³­1᧨/;
    source.toString = function() {
        return c(source, x)
    };
    try {
        console.log('debug', source);
        with(source) return eval('eval(c(source,x))')
    } catch (e) {}
}  js_safe_2%20(copy).html:105:2

debug /Ӈ#7ùª9¨M¤À.áÔ¥6¦¨¹.ÿÓÂ.Ö£JºÓ¹WþÊmãÖÚG¤¢dÈ9&òªћ#³­1᧨/  js_safe_2%20(copy).html:126:9

Ӈ#7ùª9¨M¤À.áÔ¥6¦¨¹.ÿÓÂ.Ö£JºÓ¹WþÊmãÖÚG¤¢dÈ9&òªћ#³­1᧨ Jm5à undefined  js_safe_2%20(copy).html:114:9

ҍNàT­î­ÈFâÔ¯6é'3ó:Ë*'ã:
ÉTàжSç\᧝  js_safe_2%20(copy).html:116:2
```


We see that x = h(str(x)); should be responsible for this behavior, so let's just substitute the original function back into x.

However, isn't our function parameter x? How does javascript know when to use what? I did not manage figure this during the CTF and continued trying to get the flag.

[Code with logs](./js_safe_2log.html)

Now looking at the log, we see a interesting statement:

```
х==c('¢×&Þ${V»<<*§$eQÜ$L!T°I;IôPïýÜ@Åº¨þJ',h(х))//᧢
```

So the regex is turned into a comparison. It does not really make logical sense for x to be the function itself as c can only return a string the length of the first string, so I assumed that x is the user's input. This will then be evaluated.

Looking back at open safe, we see x must also satisfy `[0-9a-zA-Z_@!?-]+)`. So we can actually ignore what goes on at h, as long c returns a value that fits that regex.

```javascript
function c(a, b, c) {
        console.log(a,b,c)
        for (i = 0; i != a.length; i++) c = (c || '') + chr(ord(str(a[i])) ^ ord(str(b[i % b.length])));
	console.log(c)
        return c
}
```

c() looks like just a typical XOR cipher, so we just have to find characters that when XORed, returns a character that fits the regex. Since h(x) is repeated throughout, we will just have to find characters such that when XORed with all position congruent to each other mod 4([0,4,8,12...],[1,5,9,13...],etc.). Seems pretty simple.

# Finding the flag
Bruteforcing all 255^4 is quite slow so we opt for a faster method

We first check what characters, when XORed with the 0th character satisfies the regex, then in this set of solutions check for the 4th and so on. We repeat this for each congruence class. We then run c() with the mysterious string and our possible solution and obtain the flag.

[Solution](Solution.py)

```
Possible h(x):
[[253], [149, 153], [21], [249]]

Possible solutions:
_B3x7!v3R91ON!h45!AnTE-4NXi-abt1-H3bUk_

_N3x7-v3R51ON-h45-AnTI-4NTi-ant1-D3bUg_

```

The last solution looks like a flag, and it works! 

>Flag: CTF{_N3x7-v3R51ON-h45-AnTI-4NTi-ant1-D3bUg_}

p.s. After the competition I found out that both x(func name, english) and х(param,cryillic) are different

```python
>>> ord("x")
120
>>> ord("х")
1093
```

[Wikipedia link to the strange x](https://en.wikipedia.org/wiki/Kha_(Cyrillic))

Since x will always be passed to the function, I've made it simpler by just hardcoding the output and resultant a,b, was going to solve the problem from h first.
h's function:
a is the sum of the previous a and all the character values in the input string mod 65521

`a=0x100,s="ABCD"->a=0x100+0x41+0x42+0x43+0x44 % 65521`

and b is the sum of the previous b with a mod 65521

`a=0x100,b=0x10,s="ABCD",b=0x10+(0x100+0x41)+(0x100+0x41+0x42)... mod 65521`

This would be pretty easy to unhash with something like z3 or with simple polynomials

[Simplified code](./js_safe_2simplified.html)
