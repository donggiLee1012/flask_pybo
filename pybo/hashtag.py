hash = {
    'brand':{
        'nike':{
            'collaboration':{
                'Off-White':{
                    'CU6015-100':{},# 러버덩크 unc
                    'CT0856-700':{} # 옾덩 남노
                },
                'Travis Scott':{
                    'CT2864-200':{},
                    'CN2405-900':{}  #스캇포스
                }
            },
            'nomalmodel':{
            }
        },
        'adidas':{
            'collaboration':{

            },
            'nomalmodel':{}
        },
        'converse':{
            'collaboration':{
                'JW Anderson':{
                    '164840C':{},# 런스타 하이 검
                    '164665C':{} #런스타 하이 흰
                }
            },
            'nomalmodel':{}
        },
        'newbalance':{
            'collaboration':{},
            'nomalmodel':{}
        },
        'jordan':{
            'collaboration':{
                'series':{
                    1:{
                        'Off-White':{

                        }
                    },
                    3:{
                       'Fragment':{

                       }
                    },
                    4:{
                        'Off-White':{

                        }
                    },
                    5:{
                        'Off-White':{}
                    },
                    6:{
                        'Travis Scott':{

                        }
                    }
                }
            }


        }
}
}

if __name__ =='__main__':
    print(hash['brand']['jordan']['series'][11])