# Singular
>Alice and Bob calculated a shared key on the elliptic curve y^2 = x^3 + 330762886318172394930696774593722907073441522749x^2 + 6688528763308432271990130594743714957884433976x + 759214505060964991648440027744756938681220132782 p = 785482254973602570424508065997142892171538672071 G = (1, 68596750097555148647236998220450053605331891340) (Alice's public key) P = d1 * G = (453762742842106273626661098428675073042272925939, 680431771406393872682158079307720147623468587944) (Bob's poblic key) Q = d2 * G = (353016783569351064519522488538358652176885848450, 287096710721721383077746502546881354857243084036) They have calculated K = d1 * d2 * G. They have taken K's x coordinate in decimal and took sha256 of it and used it for AES ECB to encrypt the flag.
>Here is the encrypted flag: 480fd106c9a637d22fddd814965742236eb314c1b8fb68e70a7c7445ff04476082f8b9026c49d27110ba41b95e9f51dc

The challenge name suggests that the elliptic curve is singular.

## Factoring

The discriminant of a elliptic curve `y^2=x^3+a2x^2+a4x+a6` is `16(-4*a2^3*a6+a2^2*a4^2+18*a2*a4*a6-4*a4^3-27*a6^2)`

The properties of the discriminant:
 - Invariance by translation
 - 0 if a repeated root exists

We notice that the discriminant of the curve given under `mod p` is `0`, meaning, under `mod p`, it can be factored into `(x-k1)(x-k1)(x-k2)` where `k1` is a repeated root of multiplicity `2` and `k2` is a root.

Applying such a factorization to the polynomial gives us a triple root:

`y^2=(x-413400541209677581972773119133520959089878607131)^3`

## Additive group

By transforming `x → x+413400541209677581972773119133520959089878607131`, the curve becomes `y^2=x^3` which is (in)famous for degenerating into the additive group via the mapping `(x, y) → x/y` and `inf → 0`

Now ECC point addition is simply adding `x/y`s together, so the DLP is trivial via modular division

> Flag: `hackim19{w0ah_math_i5_quite_fun_a57f8e21}`
