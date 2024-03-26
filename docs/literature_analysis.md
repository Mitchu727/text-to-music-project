| Model | Paper | Github | Can be run locally | Evaluation methods | Compute power needed |
|---|---|---|---|---|---|
| MusicGen | [arxiv](https://arxiv.org/abs/2306.05284) | [github](https://github.com/facebookresearch/audiocraft/blob/main/docs/MUSICGEN.md) | running through the api fails on windows but is possible run with the use of transformers library | Evaluated on MusicCaps from https://arxiv.org/abs/2301.11325 using Fréchet Audio Distance,  Kullback-Leiber Divergence and CLAP (section 3.3 of the paper), it was also evaluated using subjective metrics, the paper also proposes a new metric called chroma cosine-similarity (section 4.2) | according to documentation 16 gb GPU needed for larger models|
| AudioLDM | [arxiv](https://arxiv.org/abs/2301.12503) | [github](https://github.com/haoheliu/AudioLDM) | ? | ? | ? |
| AudioLDM2 | [arxiv](https://arxiv.org/abs/2308.05734) | [github](https://github.com/haoheliu/audioldm2) | ? | ? | ? |
| AudioGen | [arxiv](https://arxiv.org/abs/2209.15352) | ? | ? | ? | ? |
| Noise2Music | [arxiv](https://arxiv.org/pdf/2302.03917.pdf) | NOT PROVIDED | NO | Model parameters were chosen based on genarated results quality. Evaluation were conducted on 16kHz waveforms. To measure the quality of generation, authors used two kinds of metrics: the Frechet Audio Distance (FAD) and the MuLan similarity score. Metrics were calculated for these three datasets: MagnaTagATune (MTAT), AudioSet-Music-Eval and MusicCaps  | Inference time for 4 Google Cloud TPU V4 with GSPMD applied (to partition the model, time reduced by more than 50%) ~151s |
| Mulan | [arxiv](https://arxiv.org/pdf/2208.12415.pdf) | ? | ? | ? | ? |
| MusicLm | [arxiv](https://arxiv.org/pdf/2301.11325.pdf) | ? | ? | ? | ? |
| Moûsai | [arxiv](https://arxiv.org/pdf/2301.11757.pdf) | ? | ? | ? | ? |
| JEN-1 | [arxiv](https://arxiv.org/abs/2308.04729) | ? | ? | ? | ? | ? |

Furhtermore it is worth to observe this repo: https://github.com/archinetai/audio-ai-timeline
