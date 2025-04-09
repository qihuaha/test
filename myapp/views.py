from .serializers import CookbookSerializer, Addresssr, CommunitySr, MaterialSr, StoreSr, Infodetailsr, OrderSr, \
    UsersSerializer
from .models import Cookbook, infodetail, Users, Communityss, Material, Store, order, Addresss
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import UpdateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from django.conf import settings
from django.db.models import Q
from openai import OpenAI
import json
import os


class RegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        # avatar_url = request.data.get("avatar_url")

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user exists
        if Users.objects.filter(username=username).exists():
            return Response({"error": "用户名已存在"}, status=status.HTTP_400_BAD_REQUEST)

        user = Users(
            username=username,
            password=make_password(password),  # Hash the password
            # avatar_url=avatar_url,
        )
        user.save()
        return Response({"message": "用户注册成功"}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Users.objects.get(username=username)
        except Users.DoesNotExist:
            return Response({"error": "无效的用户名或密码"}, status=status.HTTP_400_BAD_REQUEST)

        if not check_password(password, user.password):
            return Response({"error": "无效的用户名或密码"}, status=status.HTTP_400_BAD_REQUEST)
        # token=jwt.encode({'user_id':user.id},settings.SECRET_KEY, algorithm='HS256')
        token = AccessToken.for_user(user)
        print(token)
        serializer = UsersSerializer(user)
        return Response({"message": "登录成功", "token": str(token), "user": serializer.data},
                        status=status.HTTP_200_OK)


class UpdateUserProfileView(UpdateAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        # 获取当前登录的用户
        return self.request.user

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response({"error": "没有找到该用户"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        # 如果请求中包含密码，则进行哈希处理
        if 'password' in request.data:
            serializer.validated_data['password'] = make_password(request.data['password'])
        serializer.save()
        updated_serializer = self.get_serializer(instance)
        return Response(updated_serializer.data, status=status.HTTP_200_OK)


# 3.10
@api_view(['DELETE'])
def delete_material(request, name):
    try:
        material = Material.objects.get(name=name)
        material.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Material.DoesNotExist:
        return Response({"error": "Material not found"}, status=status.HTTP_404_NOT_FOUND)


# 2.15
class CookbookVideoView(APIView):
    def get(self, request, *args, **kwargs):
        # 获取所有菜谱的视频 URL 列表以及名称
        cookbooks = Cookbook.objects.all()
        video_data = []  # 存储视频名称和视频 URL 的字典

        for cookbook in cookbooks:
            # 将每个菜谱名称和视频 URL 添加到字典中
            video_data.append({
                'cookbook_name': cookbook.cookbook_name,  # 菜谱名称
                'video_url': cookbook.videos  # 视频链接
            })

        return Response({'videos': video_data})


# +++++++++++++++++++++++++++++++++++++++++
@csrf_exempt
def get_recipes_by_materials(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            materials = data.get('materials', [])
            if not materials:
                return JsonResponse({'error': 'No materials provided'}, status=400)

            # 构造查询条件，逐一匹配每个食材
            query = Q()
            for material in materials:
                query |= Q(food__icontains=material)

            # 查询匹配的菜谱
            recipes = Cookbook.objects.filter(query).values('cookbook_id', 'cookbook_name', 'images', 'food')

            return JsonResponse(list(recipes), safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


# 999999999999999999999999999999999999999999
class UploadImageView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        # 获取图片和评论
        file = request.FILES.get('image')
        text = request.data.get('text')

        if not file:
            return Response({"message": "未接收到文件"}, status=400)

        if not text:
            return Response({"message": "未接收到文案"}, status=400)

        # 保存文件到 media
        file_path = default_storage.save(os.path.join('images', file.name), file)
        file_url = os.path.join(settings.MEDIA_URL, file_path)

        image_text = Communityss(images=file_url, content=text)

        image_text.save()

        return Response({"message": "文件上传成功", "file_url": file_url, "text": text}, status=200)


# 33333333333333

class CookbookLikesView(APIView):
    def get(self, request, cookbook_id):
        try:
            cookbook = Cookbook.objects.get(cookbook_id=cookbook_id)
            serializer = CookbookSerializer(cookbook)
            return Response(serializer.data)
        except Cookbook.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, cookbook_id):
        try:
            cookbook = Cookbook.objects.get(cookbook_id=cookbook_id)
            cookbook.likes = request.data.get('likes', cookbook.likes)
            cookbook.save()
            serializer = CookbookSerializer(cookbook)
            return Response(serializer.data)
        except Cookbook.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)


# 11111111111111111111111111111111111111111111


@api_view(['POST'])
def submit_material(request):
    if request.method == 'POST':
        serializer = MaterialSr(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['POST'])
def submit_order(request):
    if request.method == 'POST':
        serializer = OrderSr(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['POST'])
def submit_address(request):
    if request.method == 'POST':
        serializer = Addresssr(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# class ChatView(APIView):
#     def post(self, request):
#         question = request.data.get('question')
#         if not question:
#             return Response({"error": "No question provided"}, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             client = OpenAI(
#                 api_key="sk-e5a63173620945c0bcd2cead9d2506ff",
#                 base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
#             )
#             completion = client.chat.completions.create(
#                 model="qwen-turbo",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
#                 messages=[
#                     {'role': 'system', 'content': 'You are a helpful assistant.'},
#                     {'role': 'user', 'content': question+'怎么制做'}
#                 ]
#             )
#             return Response({"answer": completion.choices[0].message.content})
#         except Exception as e:
#             print(f"错误信息：{e}")

class ChatView(APIView):
    def post(self, request):
        # 获取菜品名称
        dish_name = request.data.get('dish_name')
        if not dish_name:
            return Response({"error": "No dish name provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 初始化 OpenAI 客户端
            client = OpenAI(
                api_key="sk-e5a63173620945c0bcd2cead9d2506ff",
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            )

            # 将菜品名称作为问题发给 OpenAI
            question = f"{dish_name} 怎么制作，详细点"

            completion = client.chat.completions.create(
                model="qwen-turbo",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
                messages=[
                    {'role': 'system', 'content': 'You are a helpful assistant.'},
                    {'role': 'user', 'content': question}
                ]
            )

            # 返回 OpenAI 的回答
            return Response({"answer": completion.choices[0].message.content})

        except Exception as e:
            print(f"错误信息：{e}")
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CookbookDetailView(APIView):
    def get(self, request, cookbook_id):
        data = Cookbook.objects.get(pk=cookbook_id)
        serializer = CookbookSerializer(data)
        return Response(serializer.data)


class Infodetailview(APIView):
    def get(self, request):
        data = infodetail.objects.all()
        serializer = Infodetailsr(data, many=True)
        return Response(serializer.data)


class StoreDetail(APIView):
    def get(self, request):
        stores = Store.objects.all()
        serializer = StoreSr(stores, many=True)
        return Response(serializer.data)


class CommunityDetailView(APIView):
    def get(self, request, community_id):
        data = Communityss.objects.get(pk=community_id)
        serializer = CommunitySr(data)
        return Response(serializer.data)


class CommunityListView(APIView):
    def get(self, request):
        communitys = Communityss.objects.all()
        serializer = CommunitySr(communitys, many=True)
        return Response(serializer.data)


class Materiallistview(APIView):
    def get(self, request):
        materials = Material.objects.all()
        serializer = MaterialSr(materials, many=True)
        return Response(serializer.data)


class Orderlv(APIView):
    def get(self, request):
        orders = order.objects.all()
        serialzer = OrderSr(orders, many=True)
        return Response(serialzer.data)


class Addresslv(APIView):
    def get(self, request):
        addresss = Addresss.objects.all()
        serialzer = Addresssr(addresss, many=True)
        return Response(serialzer.data)


class CookbookListView(APIView):
    def get(self, request):
        cookbooks = Cookbook.objects.all()
        serializer = CookbookSerializer(cookbooks, many=True)
        return Response(serializer.data)
# mysql -u root -p rkWyvSsKSCkNiwwGJDgzLLFRfWnrNDUm -h maglev.proxy.rlwy.net -P 54603 railway < backup.sql
