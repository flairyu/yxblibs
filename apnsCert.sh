#!/bin/sh

#  apnsCert.sh
#  iUM
#
#  Created by yyyy on 11-5-13.
#  Copyright 2011年 yy. All rights reserved.

# 1. 打开你的键链
# 2. 单击My Certificates
# 3. 单击Apple Development Push Services证书旁边的箭头展开它
# 4. 右键菜单中选择Export，将它保存为apns_cert.p12
# 5. 对私钥执行相同的操作并将其命名为apns_key.p12。过程中提示的密码最好使用简单密码(此处为123)，将在以后用到。
# 6. 需要合并键和证书为pem格式，使用以下命令
if [ $# -lt 3 ]; then
	echo "usage:" 
	echo "$0 apns_cert.p12 apns_key.p12 apns.pem"
    exit 0
fi

echo "(1/5) change $1 file to $1.pem"
openssl pkcs12 -clcerts -nokeys -out $1.pem -in $1
echo "(2/5) change $2 file to $2.pem"
openssl pkcs12 -nocerts -out $2.pem -in $2
# 7. 要删除apns_key.p12文件的密码，使用命令：
echo "(3/5) delete password of $2.pem"
openssl rsa -in $2.pem -out $2.unenc.pem
# 8. 最后需要使用cat命令来合并这两个文件。
echo "(4/5) compose $1.pem and $2.unenc.pem to $3"
cat $1.pem $2.unenc.pem > $3
echo "(5/5) clean all"
rm $1.pem $2.pem $2.unenc.pem
echo "done."