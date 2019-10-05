from onvif import ONVIFCamera


class CameraOnvifConnection(object):
    def __init__(self, host, port, username, password, wsdl_dir):
        self.__media_service = None

        self.connection = ONVIFCamera(
            host,
            port,
            username,
            password,
            wsdl_dir
        )

        self.connection.devicemgmt.GetDeviceInformation()

    def get_rtsp_url(self, profile_number):
        media_service = self.__get_media_service()

        profiles = media_service.GetProfiles()

        token = profiles[profile_number].token

        url_info = media_service.GetStreamUri({
            'StreamSetup': {
                'Stream': 'RTP-Unicast',
                'Transport': 'UDP'
            },
            'ProfileToken': token
        })

        return url_info.Uri

    def __get_media_service(self):
        if self.__media_service == None:
            self.__media_service = self.connection.create_media_service()

        return self.__media_service
