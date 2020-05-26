#{"commsHubId":"AD-00-00-00-00-0F-41-65","businessTargetId":"AD-00-00-FD-00-0F-41-65"},
def main():
    gfp = open("c:\\users\\devanek\\downloads\\guids50K.csv", "r")
    wfp = open("c:\\users\\devanek\\downloads\\output.csv", "w")
    for bits in gfp:
        line = bits.split(',')
        print('{"commsHubId":"' + line[0] + '","businessTargetId":"' + line[1].rstrip('\n') + '"},')
        wfp.writelines('{"commsHubId":"' + line[0] + '","businessTargetId":"' + line[1].rstrip('\n') + '"},'+"\n")
    gfp.close()
    wfp.close()

if __name__ == '__main__':
    main()
