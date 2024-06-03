import random, time, json

from agora_token_builder import RtcTokenBuilder

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import RoomMember


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


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)

    member, created = RoomMember.objects.get_or_create(
        name=data["name"],
        uid=data["UID"],
        room_name=data["room_name"],
    )

    return JsonResponse({"name": data["name"]}, safe=False)


def getMember(request):
    uid = request.GET.get("UID")
    room_name = request.GET.get("room_name")

    member = RoomMember.objects.get(uid=uid, room_name=room_name)

    name = member.name

    return JsonResponse({"name": name}, safe=False)


@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)

    member = RoomMember.objects.get(
        uid=data["UID"], name=data["name"], room_name=data["room_name"]
    )
    member.delete()

    return JsonResponse("Member deleted successfully!", safe=False)
