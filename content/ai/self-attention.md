---
title: Self Attention for Convolutional Neuronal Networks
slug: attention
summary: Self Attention can help Neuronal Networks to understand long term dependencies. With normal convolutions this can be difficult, as the receptive field is small. 
--- 

Self Attention can help Neuronal Networks to understand long term dependencies. With normal convolutions this can be difficult, as the receptive field is small. 

Self-Attention GAN (SAGAN) by [@zhang2019self] introduces an self attention mechanism to convolutional GANs leading to clearer features. The issue is that convolutions are good at local information, but the receptive fields are not large enough to include bigger structures. Instead of increasing filter sizes, we calculate the self attention. 



<svg viewBox="0 0 1555 556" xmlns="http://www.w3.org/2000/svg" fill-rule="evenodd" clip-rule="evenodd" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="1.5"><g font-family="'ArialMT','Arial',sans-serif" font-size="29.3"><text x="78.8" y="117" transform="translate(-46 3)">convolution</text><text x="46.2" y="151.9" transform="translate(-46 3)">feature maps (x)</text></g><text x="40" y="117" font-family="'ArialMT','Arial',sans-serif" font-size="29.3" transform="translate(392 122)">g(x)</text><text x="40" y="117" font-family="'ArialMT','Arial',sans-serif" font-size="29.3" transform="translate(393 326)">h(x)</text><text x="44.1" y="117" font-family="'ArialMT','Arial',sans-serif" font-size="29.3" transform="translate(392 -86)">f(x)</text><text x="40.8" y="117" font-family="'ArialMT','Arial',sans-serif" font-size="29.3" transform="translate(1270 180)">v(x)</text><circle cx="876.5" cy="236.5" r="19.5" fill="none" stroke="#000" stroke-width="4.8" transform="rotate(90 862 438) scale(.84044)"/><path d="M1113 302l-23 23M1090 301l23 24" fill="none" stroke="#000" stroke-width="4"/><circle cx="876.5" cy="236.5" r="19.5" fill="none" stroke="#000" stroke-width="4.8" transform="rotate(90 785 240) scale(.84044)"/><path d="M838 180l-24 23M814 180l23 23" fill="none" stroke="#000" stroke-width="4"/><text x="88.6" y="117" font-family="'ArialMT','Arial',sans-serif" font-size="29.3" transform="translate(613 -34)">transpose</text><text x="101.7" y="117" font-family="'ArialMT','Arial',sans-serif" font-size="29.3" transform="translate(786 63)">softmax</text><text x="113" y="110.3" font-family="'ArialMT','Arial',sans-serif" font-size="20" transform="translate(1115 266)">1x1 conv</text><text x="40" y="110.3" font-family="'ArialMT','Arial',sans-serif" font-size="20" transform="translate(272 -4)">1x1 conv</text><text x="40" y="110.3" font-family="'ArialMT','Arial',sans-serif" font-size="20" transform="translate(272 206)">1x1 conv</text><text x="40" y="110.3" font-family="'ArialMT','Arial',sans-serif" font-size="20" transform="translate(272 405)">1x1 conv</text><g font-family="'ArialMT','Arial',sans-serif" font-size="29.3"><text x="96.7" y="117" transform="translate(951 -12)">attention</text><text x="124.5" y="151.9" transform="translate(951 -12)">map</text></g><g font-family="'ArialMT','Arial',sans-serif" font-size="29.3"><text x="69.8" y="117" transform="translate(1295 50)">self attention</text><text x="45.4" y="147.3" transform="translate(1295 50)">feature maps (o)</text></g><path fill="#fff" stroke="#fff200" stroke-width="4.003281" d="M556 7h76v77h-76z"/><path d="M556 33h76M556 58h76M581 7v77M607 7v77" fill="none" stroke="#fff200" stroke-width="4.003281"/><g><path fill="#fff" stroke="#fff200" stroke-width="4.003281" d="M556 7h76v77h-76z"/><path d="M556 33h76M556 58h76M581 7v77M607 7v77" fill="none" stroke="#fff200" stroke-width="4.003281"/></g><g><path fill="#fff" stroke="#000bff" stroke-width="4.166016" d="M45 169h76v77H45z"/><path d="M45 195h76M45 220h76M70 169v77M96 169v77" fill="none" stroke="#000bff" stroke-width="4.166016"/><g><path fill="#fff" stroke="#000bff" stroke-width="4.166016" d="M45 169h76v77H45z"/><path d="M45 195h76M45 220h76M70 169v77M96 169v77" fill="none" stroke="#000bff" stroke-width="4.166016"/></g><g><path fill="#fff" stroke="#000bff" stroke-width="4.166016" d="M70 193h77v77H70z"/><path d="M70 219h77M70 244h77M95 193v77M121 193v77" fill="none" stroke="#000bff" stroke-width="4.166016"/><g><path fill="#fff" stroke="#000bff" stroke-width="4.166016" d="M70 193h77v77H70z"/><path d="M70 219h77M70 244h77M95 193v77M121 193v77" fill="none" stroke="#000bff" stroke-width="4.166016"/></g></g><g><path fill="#fff" stroke="#000bff" stroke-width="4.166016" d="M96 218h77v77H96z"/><path d="M96 244h77M96 269h77M121 218v77M147 218v77" fill="none" stroke="#000bff" stroke-width="4.166016"/><g><path fill="#fff" stroke="#000bff" stroke-width="4.166016" d="M96 218h77v77H96z"/><path d="M96 244h77M96 269h77M121 218v77M147 218v77" fill="none" stroke="#000bff" stroke-width="4.166016"/></g></g></g><g><path fill="#fff" stroke="#18a621" stroke-width="4.003281" d="M556 218h76v77h-76z"/><path d="M556 244h76M556 269h76M581 218v77M607 218v77" fill="none" stroke="#18a621" stroke-width="4.003281"/><g><path fill="#fff" stroke="#18a621" stroke-width="4.003281" d="M556 218h76v77h-76z"/><path d="M556 244h76M556 269h76M581 218v77M607 218v77" fill="none" stroke="#18a621" stroke-width="4.003281"/></g><g><path fill="#fff" stroke="#18a621" stroke-width="4.003281" d="M581 242h77v77h-77z"/><path d="M581 268h77M581 293h77M606 242v77M632 242v77" fill="none" stroke="#18a621" stroke-width="4.003281"/><g><path fill="#fff" stroke="#18a621" stroke-width="4.003281" d="M581 242h77v77h-77z"/><path d="M581 268h77M581 293h77M606 242v77M632 242v77" fill="none" stroke="#18a621" stroke-width="4.003281"/></g></g><g><path fill="#fff" stroke="#18a621" stroke-width="4.003281" d="M607 267h77v77h-77z"/><path d="M607 293h77M607 318h77M632 267v77M658 267v77" fill="none" stroke="#18a621" stroke-width="4.003281"/><g><path fill="#fff" stroke="#18a621" stroke-width="4.003281" d="M607 267h77v77h-77z"/><path d="M607 293h77M607 318h77M632 267v77M658 267v77" fill="none" stroke="#18a621" stroke-width="4.003281"/></g></g></g><g><path fill="#fff" stroke="#a026de" stroke-width="4.003281" d="M556 419h76v77h-76z"/><path d="M556 445h76M556 471h76M581 419v77M607 419v77" fill="none" stroke="#a026de" stroke-width="4.003281"/><g><path fill="#fff" stroke="#a026de" stroke-width="4.003281" d="M556 419h76v77h-76z"/><path d="M556 445h76M556 471h76M581 419v77M607 419v77" fill="none" stroke="#a026de" stroke-width="4.003281"/></g><g><path fill="#fff" stroke="#a026de" stroke-width="4.003281" d="M581 443h77v77h-77z"/><path d="M581 469h77M581 495h77M606 443v77M632 443v77" fill="none" stroke="#a026de" stroke-width="4.003281"/><g><path fill="#fff" stroke="#a026de" stroke-width="4.003281" d="M581 443h77v77h-77z"/><path d="M581 469h77M581 495h77M606 443v77M632 443v77" fill="none" stroke="#a026de" stroke-width="4.003281"/></g></g><g><path fill="#fff" stroke="#a026de" stroke-width="4.003281" d="M607 468h77v77h-77z"/><path d="M607 494h77M607 520h77M632 468v77M658 468v77" fill="none" stroke="#a026de" stroke-width="4.003281"/><g><path fill="#fff" stroke="#a026de" stroke-width="4.003281" d="M607 468h77v77h-77z"/><path d="M607 494h77M607 520h77M632 468v77M658 468v77" fill="none" stroke="#a026de" stroke-width="4.003281"/></g></g></g><g><path fill="#fff" stroke="#df7f10" stroke-width="4.003281" d="M1401 251h76v77h-76z"/><path d="M1401 276h76M1401 302h76M1426 251v77M1452 251v77" fill="none" stroke="#df7f10" stroke-width="4.003281"/><g><path fill="#fff" stroke="#df7f10" stroke-width="4.003281" d="M1401 251h76v77h-76z"/><path d="M1401 276h76M1401 302h76M1426 251v77M1452 251v77" fill="none" stroke="#df7f10" stroke-width="4.003281"/></g></g><g><path fill="#fff" stroke="#fff200" stroke-width="4.003281" d="M581 31h77v77h-77z"/><path d="M581 57h77M581 82h77M606 31v77M632 31v77" fill="none" stroke="#fff200" stroke-width="4.003281"/><g><path fill="#fff" stroke="#fff200" stroke-width="4.003281" d="M581 31h77v77h-77z"/><path d="M581 57h77M581 82h77M606 31v77M632 31v77" fill="none" stroke="#fff200" stroke-width="4.003281"/></g></g><g><path fill="#fff" stroke="#df7f10" stroke-width="4.003281" d="M1426 275h77v77h-77z"/><path d="M1426 301h77M1426 326h77M1451 275v77M1477 275v77" fill="none" stroke="#df7f10" stroke-width="4.003281"/><g><path fill="#fff" stroke="#df7f10" stroke-width="4.003281" d="M1426 275h77v77h-77z"/><path d="M1426 301h77M1426 326h77M1451 275v77M1477 275v77" fill="none" stroke="#df7f10" stroke-width="4.003281"/></g></g><g><path fill="#fff" stroke="#fff200" stroke-width="4.003281" d="M607 56h77v77h-77z"/><path d="M607 82h77M607 107h77M632 56v77M658 56v77" fill="none" stroke="#fff200" stroke-width="4.003281"/><g><path fill="#fff" stroke="#fff200" stroke-width="4.003281" d="M607 56h77v77h-77z"/><path d="M607 82h77M607 107h77M632 56v77M658 56v77" fill="none" stroke="#fff200" stroke-width="4.003281"/></g></g><g><path fill="#fff" stroke="#df7f10" stroke-width="4.003281" d="M1452 300h77v77h-77z"/><path d="M1452 325h77M1452 351h77M1477 300v77M1503 300v77" fill="none" stroke="#df7f10" stroke-width="4.003281"/><g><path fill="#fff" stroke="#df7f10" stroke-width="4.003281" d="M1452 300h77v77h-77z"/><path d="M1452 325h77M1452 351h77M1477 300v77M1503 300v77" fill="none" stroke="#df7f10" stroke-width="4.003281"/></g></g><g><path d="M326 54l12-6-3 13-9-7z"/><path d="M187 252L332 56" fill="none" stroke="#000" stroke-width="4"/></g><g><path d="M339 446l2 13-12-6 10-7z"/><path d="M187 253l148 198" fill="none" stroke="#000" stroke-width="4"/></g><g><path d="M326 246l13 6-12 6-1-12z"/><path d="M187 253l142-1" fill="none" stroke="#000" stroke-width="4"/></g><g><path d="M1050 184l12 6-12 6v-12z"/><path d="M842 192l210-2" fill="none" stroke="#000" stroke-width="4"/></g><g><path d="M1095 283l6 12 6-12h-12z"/><path d="M1101 285v-62" fill="none" stroke="#000" stroke-width="4"/></g><g><path d="M541 448l12 6-12 6v-12z"/><path d="M367 454h177" fill="none" stroke="#000" stroke-width="4"/></g><g><path d="M1095 341l6-12 6 12h-12z"/><path d="M690 504h411V339" fill="none" stroke="#000" stroke-width="4"/></g><g><path d="M820 222l6-12 6 12h-12z"/><path d="M690 309h136v-89" fill="none" stroke="#000" stroke-width="4"/></g><g><path d="M832 161l-6 12-6-12h12z"/><path d="M690 93h136v71" fill="none" stroke="#000" stroke-width="4"/></g><g><path d="M540 39l12 6-12 6V39z"/><path d="M367 45h176" fill="none" stroke="#000" stroke-width="4"/></g><g><path d="M541 247l12 6-12 6v-12z"/><path d="M367 252l177 1" fill="none" stroke="#000" stroke-width="4"/></g><g><path fill="#fff" stroke="#000" stroke-width="1.3" d="M1256 273h25v84h-25z"/></g><g><path fill="#fff" stroke="#000" stroke-width="1.3" d="M339 4h26v84h-26z"/></g><g><path fill="#fff" stroke="#000" stroke-width="1.3" d="M339 214h26v84h-26z"/></g><g><path fill="#fff" stroke="#000" stroke-width="1.3" d="M339 413h26v84h-26z"/></g><g><path d="M1244 318l12-6-12-6v12z"/><path d="M1246 312h-128" fill="none" stroke="#000" stroke-width="4"/></g><g><path d="M1387 318l12-6-12-6v12z"/><path d="M1389 312h-106" fill="none" stroke="#000" stroke-width="4"/></g><g><path fill="#e6e6e6" stroke="#000" stroke-width="1.3" d="M1062 148h26v25h-26z"/><path fill="#a6a6a6" stroke="#000" stroke-width="1.3" d="M1088 148h26v25h-26z"/><path fill="#666" stroke="#000" stroke-width="1.3" d="M1114 148h26v25h-26z"/><path fill="#fff" stroke="#000" stroke-width="1.3" d="M1062 173h26v25h-26z"/><path fill="#1a1a1a" stroke="#000" stroke-width="1.3" d="M1088 173h26v25h-26z"/><path fill="#e6e6e6" stroke="#000" stroke-width="1.3" d="M1114 173h26v25h-26z"/><path fill="#b3b3b3" stroke="#000" stroke-width="1.3" d="M1062 198h26v25h-26z"/><path fill="gray" stroke="#000" stroke-width="1.3" d="M1088 198h26v25h-26z"/><path fill="#333" stroke="#000" stroke-width="1.3" d="M1114 198h26v25h-26z"/></g></svg>
*Structure of Self-Attention in CNN-Networks [Adapted from: [@zhang2019self]]* 

$f$ also called the Query Layer (produced by a size 1 conv) is transposed and than combined with $g$ the Key layer via Dot Product to form the attention map. The Attention map defines the attention score between two pixels. This means how much attentions do we pay to region $i$ when synthesizing $j$.   By combining $h$ and the Attention map (via Dot Product) one gets the Attention Feature Maps (or Attention Weights).


To calculate the output we add the attention weight (scaled by a factor $\gamma$) to the input feature $\boldsymbol{y}_{\boldsymbol{i}}=\gamma \boldsymbol{o}_{\boldsymbol{i}}+\boldsymbol{x}_{\boldsymbol{i}}$. By starting with $\gamma = 0$, we focus on local neighorhoods and then increase it to shift attention to the bigger contexts.

Check out the [fastai-Code](https://github.com/fastai/fastai/blob/75f4c17dc019aee9a0af08bd458a56e00d7393f8/fastai/layers.py#L288) to get an idea for the implementation.