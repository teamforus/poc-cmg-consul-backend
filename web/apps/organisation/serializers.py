from rest_framework import serializers


class CreateLoginSerializer(serializers.Serializer):
    public_key = serializers.CharField(
        max_length=200, required=True,)

    def validate(self, attrs):

        self.public_key = attrs['public_key']
        return attrs