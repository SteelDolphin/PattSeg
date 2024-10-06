I = imread('./pattern/01.jpg');
imshow(I)
title('Original Image')

E = entropyfilt(I);
S = stdfilt(I,ones(9));
R = rangefilt(I,ones(9));

Eim = rescale(E);
Sim = rescale(S);

montage({Eim,Sim,R},'Size',[1 3],'BackgroundColor','w',"BorderSize",20)
title('Texture Images Showing Local Entropy, Local Standard Deviation, and Local Range')

BW1 = imbinarize(Eim,0.8);
imshow(BW1)
title('Thresholded Texture Image')

BWao = bwareaopen(BW1,2000);
imshow(BWao)
title('Area-Opened Texture Image')

