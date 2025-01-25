import re
from ..web import agentInfo
from django.utils.deprecation import MiddlewareMixin

class MobileDetectionMiddleware(MiddlewareMixin):

    def process_request(self, request):
        isSmartPhone = False
        isMobile = False
        isTablet = False
        isIphone = False
        isAndroid = False

        user_agent = request.META.get("HTTP_USER_AGENT")
        http_accept = request.META.get("HTTP_ACCEPT")

        if user_agent and http_accept:
            agent = agentInfo.AgentInfo(userAgent=user_agent, httpAccept=http_accept)
            isTablet = agent.detectTierTablet()
            isIphone = agent.detectTierIphone()
            isAndroid = agent.detectAndroidPhone()
            isSmartPhone  = isIphone or isAndroid
            isMobile = isTablet or isIphone or isAndroid or agent.detectMobileQuick()
    
        request.isSmartPhone = isSmartPhone
        request.isMobile = isMobile
        request.isTablet = isTablet
        request.isIphone = isIphone
        request.isAndroid = isAndroid

        return None