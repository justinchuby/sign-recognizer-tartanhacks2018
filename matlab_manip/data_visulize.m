filename = '../sign_language/hello/untitled folder/orientationEuler-1518213083.csv';
A = csvread(filename,1,1);

filename_gyro = '../sign_language/hello/untitled folder/gyro-1518213083.csv';
B = csvread(filename_gyro,1,1);
% disp(A);

roll = transpose(A(:,1));
pitch = transpose(A(:,2));
yaw = transpose(A(:,3));

x = transpose(B(:,1));
y = transpose(B(:,2));
z = transpose(B(:,3));



figure,
subplot(1,2,1);
plot3(roll,pitch,yaw);
subplot(1,2,2);
fsurf(x,y,z);
% [Xmesh,Ymesh,Zmesh] = meshgrid(roll,pitch,yaw);
% f = Xmesh.^2 + Ymesh.^2 + Zmesh.^2;
% % figure, surf(roll, pitch, yaw);
% sliceomatic(f,roll, pitch, yaw)