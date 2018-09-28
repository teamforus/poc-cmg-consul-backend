from rest_framework import serializers


class CreateLoginSerializer(serializers.Serializer):
    public_key = serializers.CharField(max_length=200, required=True)

    def validate(self, attrs):

        self.public_key = attrs['public_key']
        return attrs


class LoginAllowSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=200, required=True)
    auth_token = serializers.CharField(max_length=200, required=True)

    is_subscribe = serializers.BooleanField(required=False, default=False)

    def validate(self, attrs):

        self.public_key = attrs['key']
        self.is_subscribe = attrs['is_subscribe']
        self.auth_token = attrs['auth_token']
        return attrs


class LoginDisallowSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=200, required=True)

    def validate(self, attrs):

        self.public_key = attrs['key']
        return attrs