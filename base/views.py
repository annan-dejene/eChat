import random, time

from django.shortcuts import render

from django.http import JsonResponse

from agora_token_builder import RtcTokenBuilder


def get_token(request):

    appId = "87adc7c547544480a6b1acaa3cb052bd"
    appCertificate = "53be29e8e5fa4b97a54b55391b96b332"
    channelName = request.GET.get("channel")
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600 * 24
    currentTimeStamp = time.time()
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1  # 1 -- host, 2 -- guest

    # Build token with uid
    token = RtcTokenBuilder.buildTokenWithUid(
        appId, appCertificate, channelName, uid, role, privilegeExpiredTs
    )

    return JsonResponse({"token": token, "uid": uid}, safe=False)


def lobby(request):
    return render(request, "base/lobby.html", {})


def room(request):
    return render(request, "base/room.html", {})
