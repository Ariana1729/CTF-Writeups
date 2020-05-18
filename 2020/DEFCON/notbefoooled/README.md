# nottobefooled

> What's the trick to not be foooled?

## Challenge

We are given a sage script that asks for a elliptic curve over a finite field with trace one(number of points is the same as modulus), then attempts to run Smart attack on it. If the attack fails, we are given the flag.

## Examples

By searching up the code for `launch_attack`, one finds a recent stack exchange post titled [Why Smart's attack doesn't work on this ECDLP?](https://crypto.stackexchange.com/questions/70454/why-smarts-attack-doesnt-work-on-this-ecdlp). This suggests when the lifted curve over p-adiac rationals is isomorphic to the curve over finite field with p elements, the attack fails. Looking at the curve, it is of the form `y^2=x^3+b`, so a possible conjecture is that anomalous curves of such form will work. In fact by finding examples of anomalous curves of such form with small modulus by brute force, one can notice that smarts attack does not work on all of these curves (at least without slight modification).

Without going into too much detail on how it works, following the notation of Section 5.4 in Lawrence C. Washington - Elliptic curves, number theory and cryptography, by looking at the curve `y^2=x^3+ap^6`, we can show that if `v_p(y)<0`, then it must be less than or equal to -6 and `v_p(x)` is less than or equal to -4. If we look at the procedure for Smart's attack in Section 5.4, we see that this implies `v_p(m_1)` and `v_p(m_2)` are necessarily negative, hence the attack, in general, does not work.

Anomalous curves of small modulus of the form `y^2=x^3+b`:

p|b
:---:|:---:
7 | 5
19 | 10
19 | 13
19 | 15
37 | 5
37 | 13
37 | 18
37 | 19
37 | 24
37 | 32
61 | 2
61 | 6
61 | 7
61 | 18
61 | 21
61 | 40
61 | 43
61 | 54
61 | 55
61 | 59

## Generating anomalous curves of the form y^2=x^3+b

Now we have identified what curve we want to generate, we need to actually generate them. A brute force search turns out to take way too long so information about what kind of primes work will be helpful. Fortunately, an old paper from 1973 has the information we want: [Hasse invariants and anomalous primes for elliptic curves with complex multiplication](https://www.sciencedirect.com/science/article/pii/0022314X76900871). By corollary 3.11, we see that if `p=12s^2+6s+1` is a prime, then anomalous curves of the form `y^2=x^3+a` exists modulo `p`
. With this we simply randomly guess values of `b` until we find one.

Random generation of values is suitable for this as such curves must exist and there are only `6` possible orders/traces. This is shown in the paper [The Orders of Elliptic Curves y^2=x^3+b, b\in F^\*\_p](http://ousar.lib.okayama-u.ac.jp/files/public/1/14126/20160527204844315776/Mem_Fac_Eng_OU_40_1_84.pdf)

This allows us to easily find anomalous curves with the Smart attack implementation failing.

> `Flag: OOO{be_Smarter_like_you_just_did}`
